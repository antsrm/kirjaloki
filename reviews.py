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
    sql = "SELECT * FROM reviews WHERE id = ?"
    return db.query_one(sql, (review_id,))

def add_review(title, author, rating, review, user_id):
    sql = """
        INSERT INTO reviews (title, author, rating, review, user_id)
        VALUES (?, ?, ?, ?, ?)
    """
    db.execute(sql, (title, author, rating, review, user_id))

def update_review(review_id, title, author, rating, review):
    sql = """
        UPDATE reviews
        SET title = ?, author = ?, rating = ?, review = ?
        WHERE id = ?
    """
    db.execute(sql, (title, author, rating, review, review_id))

def delete_review(review_id):
    sql = "DELETE FROM reviews WHERE id = ?"
    db.execute(sql, (review_id,))

def search_reviews(query):
    sql = """
        SELECT *
        FROM reviews
        WHERE title LIKE ? OR author LIKE ? OR review LIKE ?
        ORDER BY id DESC
    """
    like_query = "%" + query + "%"
    return db.query(sql, (like_query, like_query, like_query))