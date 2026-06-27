from flask import Flask, render_template, request, redirect, session, abort
import secrets
import reviews
import users
import genres
import comments
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "dev"

@app.before_request
def ensure_csrf_token():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(16)

def check_csrf():
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

def format_timestamp(timestamp):
    dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    dt = dt + timedelta(hours=3)
    return dt.strftime("%d.%m.%Y %H:%M")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    check_csrf()

    username = request.form["username"]
    password = request.form["password"]

    if not username.strip():
        return render_template(
            "register.html",
            error="Käyttäjätunnus ei voi olla tyhjä"
        )

    if not password.strip():
        return render_template(
            "register.html",
            error="Salasana ei voi olla tyhjä"
        )

    if users.get_user_by_username(username):
        return render_template(
            "register.html",
            error="Käyttäjätunnus on jo käytössä",
            username=username
        )

    users.create_user(username, password)

    return redirect("/login?registered=1")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        registered = request.args.get("registered")

        return render_template(
            "login.html",
            registered=registered,
            error=None
        )

    check_csrf()

    username = request.form["username"]
    password = request.form["password"]

    user = users.check_login(username, password)

    if not user:
        return render_template(
            "login.html",
            registered=None,
            error="Väärä tunnus tai salasana"
        )

    session["user_id"] = user["id"]
    session["username"] = user["username"]

    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/reviews")
def show_reviews():
    genre_id = request.args.get("genre_id")
    all_genres = genres.get_genres()

    if genre_id:
        all_reviews = reviews.get_reviews_by_genre(genre_id)
    else:
        all_reviews = reviews.get_reviews()

    formatted_reviews = []
    review_genres = {}

    for review in all_reviews:
        review = dict(review)
        review["created_at"] = format_timestamp(review["created_at"])

        formatted_reviews.append(review)
        review_genres[review["id"]] = genres.get_review_genre_names(review["id"])

    return render_template(
        "reviews.html",
        reviews=formatted_reviews,
        genres=all_genres,
        selected_genre_id=genre_id,
        review_genres=review_genres
    )

@app.route("/new_review", methods=["GET", "POST"])
def new_review():
    if "user_id" not in session:
        return redirect("/login")

    all_genres = genres.get_genres()

    if request.method == "GET":
        return render_template(
            "new_review.html",
            genres=all_genres,
            error=None,
            form_data={},
            selected_genre_ids=[]
        )

    check_csrf()

    title = request.form["title"]
    author = request.form["author"]
    rating = request.form["rating"]
    review = request.form["review"]
    genre_ids = list(dict.fromkeys(request.form.getlist("genres")))
    selected_genre_ids = [int(genre_id) for genre_id in genre_ids]

    form_data = {
        "title": title,
        "author": author,
        "rating": rating,
        "review": review
    }

    if not title.strip():
        return render_template(
            "new_review.html",
            genres=all_genres,
            error="Kirjan nimi ei voi olla tyhjä",
            form_data=form_data,
            selected_genre_ids=selected_genre_ids
        )

    if not author.strip():
        return render_template(
            "new_review.html",
            genres=all_genres,
            error="Kirjailija ei voi olla tyhjä",
            form_data=form_data,
            selected_genre_ids=selected_genre_ids
        )

    if not rating.strip():
        return render_template(
            "new_review.html",
            genres=all_genres,
            error="Arvosana ei voi olla tyhjä",
            form_data=form_data,
            selected_genre_ids=selected_genre_ids
        )

    if not review.strip():
        return render_template(
            "new_review.html",
            genres=all_genres,
            error="Arvio ei voi olla tyhjä",
            form_data=form_data,
            selected_genre_ids=selected_genre_ids
        )

    if len(genre_ids) > 5:
        return render_template(
            "new_review.html",
            genres=all_genres,
            error="Voit valita enintään 5 genreä",
            form_data=form_data,
            selected_genre_ids=selected_genre_ids
        )

    review_id = reviews.add_review(
        title.strip(),
        author.strip(),
        rating,
        review.strip(),
        session["user_id"]
    )

    genres.add_review_genres(review_id, genre_ids)

    return redirect("/reviews")

@app.route("/edit_review/<int:review_id>", methods=["GET", "POST"])
def edit_review(review_id):
    if "user_id" not in session:
        return redirect("/login")

    review = reviews.get_review(review_id)

    if review["user_id"] != session["user_id"]:
        return "Ei oikeutta muokata tätä arviota"

    all_genres = genres.get_genres()
    review_genres = genres.get_review_genres(review_id)
    selected_genre_ids = [genre["id"] for genre in review_genres]

    if request.method == "GET":
        return render_template(
            "edit_review.html",
            review=review,
            genres=all_genres,
            selected_genre_ids=selected_genre_ids,
            error=None
        )

    check_csrf()

    title = request.form["title"]
    author = request.form["author"]
    rating = request.form["rating"]
    review_text = request.form["review"]
    genre_ids = list(dict.fromkeys(request.form.getlist("genres")))
    selected_genre_ids = [int(genre_id) for genre_id in genre_ids]

    if len(genre_ids) > 5:
        edited_review = {
            "id": review_id,
            "title": title,
            "author": author,
            "rating": rating,
            "review": review_text,
            "user_id": session["user_id"]
        }

        return render_template(
            "edit_review.html",
            review=edited_review,
            genres=all_genres,
            selected_genre_ids=selected_genre_ids,
            error="Voit valita enintään 5 genreä"
        )

    reviews.update_review(review_id, title, author, rating, review_text)

    genres.delete_review_genres(review_id)
    genres.add_review_genres(review_id, genre_ids)

    return redirect("/reviews")

@app.route("/delete_review/<int:review_id>", methods=["GET", "POST"])
def delete_review(review_id):
    if "user_id" not in session:
        return redirect("/login")

    review = reviews.get_review(review_id)

    if not review:
        return "Arviota ei löytynyt"

    if review["user_id"] != session["user_id"]:
        return "Ei oikeutta poistaa tätä arviota"

    if request.method == "GET":
        return render_template(
            "confirm_delete.html",
            title="Poista arvio",
            message="Haluatko varmasti poistaa tämän arvion?",
            item_name=review["title"],
            action_url="/delete_review/" + str(review_id),
            cancel_url="/review/" + str(review_id),
            confirm_button="Poista arvio"
        )

    check_csrf()

    reviews.delete_review(review_id)

    return redirect("/reviews")

@app.route("/search")
def search():
    query = request.args.get("query", "")
    review_results = []
    user_results = []
    review_genres = {}

    if query:
        review_results = reviews.search_reviews(query)
        user_results = users.search_users(query)

        for review in review_results:
            review_genres[review["id"]] = genres.get_review_genre_names(review["id"])

    return render_template(
        "search.html",
        query=query,
        reviews=review_results,
        users=user_results,
        review_genres=review_genres
    )

@app.route("/review/<int:review_id>")
def show_review(review_id):
    review = reviews.get_review(review_id)

    if not review:
        return "Arviota ei löytynyt"

    review = dict(review)
    review["created_at"] = format_timestamp(review["created_at"])

    review_genres = genres.get_review_genre_names(review_id)

    review_comments = comments.get_comments(review_id)
    formatted_comments = []

    for comment in review_comments:
        comment = dict(comment)
        comment["created_at"] = format_timestamp(comment["created_at"])
        formatted_comments.append(comment)

    return render_template(
        "review.html",
        review=review,
        review_genres=review_genres,
        comments=formatted_comments
    )

@app.route("/user/<int:user_id>")
def user_page(user_id):
    user = users.get_user(user_id)

    if not user:
        return "Käyttäjää ei löytynyt"

    user_reviews = reviews.get_reviews_by_user(user_id)
    review_count = reviews.count_reviews_by_user(user_id)
    average_rating = reviews.get_average_rating_by_user(user_id)

    return render_template(
        "user.html",
        user=user,
        reviews=user_reviews,
        review_count=review_count,
        average_rating=average_rating
    )

@app.route("/add_comment/<int:review_id>", methods=["POST"])
def add_comment(review_id):
    if "user_id" not in session:
        return redirect("/login")

    check_csrf()

    comment = request.form["comment"]

    if not comment.strip():
        return redirect("/review/" + str(review_id))

    comments.add_comment(review_id, session["user_id"], comment)

    return redirect("/review/" + str(review_id))

@app.route("/delete_comment/<int:comment_id>", methods=["GET", "POST"])
def delete_comment(comment_id):
    if "user_id" not in session:
        return redirect("/login")

    comment = comments.get_comment(comment_id)

    if not comment:
        return "Kommenttia ei löytynyt"

    if comment["user_id"] != session["user_id"]:
        return "Ei oikeutta poistaa tätä kommenttia"

    if request.method == "GET":
        return render_template(
            "confirm_delete.html",
            title="Poista kommentti",
            message="Haluatko varmasti poistaa tämän kommentin?",
            item_name=comment["comment"][:80],
            action_url="/delete_comment/" + str(comment_id),
            cancel_url="/review/" + str(comment["review_id"]),
            confirm_button="Poista kommentti"
        )

    check_csrf()

    comments.delete_comment(comment_id)

    return redirect("/review/" + str(comment["review_id"]))

@app.route("/delete_user/<int:user_id>", methods=["GET", "POST"])
def delete_user(user_id):
    if "user_id" not in session:
        return redirect("/login")

    if session["user_id"] != user_id:
        return "Ei oikeutta poistaa tätä käyttäjää"

    user = users.get_user(user_id)

    if not user:
        return "Käyttäjää ei löytynyt"

    if request.method == "GET":
        return render_template(
            "confirm_delete.html",
            title="Poista käyttäjätili",
            message="Haluatko varmasti poistaa käyttäjätilisi? Tämä poistaa myös kaikki arviosi ja kommenttisi.",
            item_name=user["username"],
            action_url="/delete_user/" + str(user_id),
            cancel_url="/user/" + str(user_id),
            confirm_button="Poista käyttäjätili"
        )

    check_csrf()

    user_reviews = reviews.get_reviews_by_user(user_id)

    for review in user_reviews:
        reviews.delete_review(review["id"])

    comments.delete_comments_by_user(user_id)
    users.delete_user(user_id)

    session.clear()

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)