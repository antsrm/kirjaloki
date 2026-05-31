from flask import Flask, render_template, request, redirect, session
import reviews
import users

app = Flask(__name__)
app.secret_key = "dev"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    username = request.form["username"]
    password = request.form["password"]

    if users.get_user_by_username(username):
        return "Käyttäjätunnus on jo käytössä"

    users.create_user(username, password)

    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form["username"]
    password = request.form["password"]

    user = users.check_login(username, password)

    if not user:
        return "Väärä tunnus tai salasana"

    session["user_id"] = user["id"]
    session["username"] = user["username"]

    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/reviews")
def show_reviews():
    all_reviews = reviews.get_reviews()
    return render_template("reviews.html", reviews=all_reviews)

@app.route("/new_review", methods=["GET", "POST"])
def new_review():
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "GET":
        return render_template("new_review.html")

    title = request.form["title"]
    author = request.form["author"]
    rating = request.form["rating"]
    review = request.form["review"]

    reviews.add_review(title, author, rating, review, session["user_id"])

    return redirect("/reviews")

@app.route("/edit_review/<int:review_id>", methods=["GET", "POST"])
def edit_review(review_id):
    if "user_id" not in session:
        return redirect("/login")

    review = reviews.get_review(review_id)

    if review["user_id"] != session["user_id"]:
        return "Ei oikeutta muokata tätä arviota"

    if request.method == "GET":
        return render_template("edit_review.html", review=review)

    title = request.form["title"]
    author = request.form["author"]
    rating = request.form["rating"]
    review_text = request.form["review"]

    reviews.update_review(review_id, title, author, rating, review_text)

    return redirect("/reviews")

@app.route("/delete_review/<int:review_id>", methods=["POST"])
def delete_review(review_id):
    if "user_id" not in session:
        return redirect("/login")

    review = reviews.get_review(review_id)

    if review["user_id"] != session["user_id"]:
        return "Ei oikeutta poistaa tätä arviota"

    reviews.delete_review(review_id)
    return redirect("/reviews")

@app.route("/search")
def search():
    query = request.args.get("query", "")
    results = []

    if query:
        results = reviews.search_reviews(query)

    return render_template("search.html", query=query, results=results)

if __name__ == "__main__":
    app.run(debug=True)