import db

def get_reviews():
    sql = """
        SELECT reviews.*, users.username
        FROM reviews
        JOIN users ON reviews.user_id = users.id
        ORDER BY reviews.id DESC
    """
    return db.query(sql)

def get_review(review_id):
    sql = """
        SELECT reviews.*, users.username
        FROM reviews
        JOIN users ON reviews.user_id = users.id
        WHERE reviews.id = ?
    """
    return db.query_one(sql, (review_id,))

def add_review(title, author, rating, review, user_id):
    sql = """
        INSERT INTO reviews (title, author, rating, review, user_id)
        VALUES (?, ?, ?, ?, ?)
    """

    con = db.get_connection()
    cursor = con.execute(
        sql,
        (title, author, rating, review, user_id)
    )

    review_id = cursor.lastrowid

    con.commit()
    con.close()

    return review_id

def update_review(review_id, title, author, rating, review):
    sql = """
        UPDATE reviews
        SET title = ?, author = ?, rating = ?, review = ?
        WHERE id = ?
    """
    db.execute(sql, (title, author, rating, review, review_id))

def delete_review(review_id):
    sql = "DELETE FROM review_genres WHERE review_id = ?"
    db.execute(sql, (review_id,))

    sql = "DELETE FROM comments WHERE review_id = ?"
    db.execute(sql, (review_id,))

    sql = "DELETE FROM reviews WHERE id = ?"
    db.execute(sql, (review_id,))

def search_reviews(query):
    sql = """
        SELECT reviews.*, users.username
        FROM reviews
        JOIN users ON reviews.user_id = users.id
        WHERE reviews.title LIKE ?
           OR reviews.author LIKE ?
           OR reviews.review LIKE ?
        ORDER BY reviews.id DESC
    """
    like_query = "%" + query + "%"
    return db.query(sql, (like_query, like_query, like_query))

def get_reviews_by_user(user_id):
    sql = """
        SELECT *
        FROM reviews
        WHERE user_id = ?
        ORDER BY id DESC
    """
    return db.query(sql, (user_id,))

def count_reviews_by_user(user_id):
    sql = """
        SELECT COUNT(*) AS count
        FROM reviews
        WHERE user_id = ?
    """
    result = db.query_one(sql, (user_id,))
    return result["count"]

def get_average_rating_by_user(user_id):
    sql = """
        SELECT AVG(rating) AS average
        FROM reviews
        WHERE user_id = ?
    """
    result = db.query_one(sql, (user_id,))
    return result["average"]

def get_reviews_by_genre(genre_id):
    sql = """
        SELECT reviews.*, users.username
        FROM reviews
        JOIN users ON reviews.user_id = users.id
        JOIN review_genres ON reviews.id = review_genres.review_id
        WHERE review_genres.genre_id = ?
        ORDER BY reviews.id DESC
    """
    return db.query(sql, (genre_id,))