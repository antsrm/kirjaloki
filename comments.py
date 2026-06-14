import db

def get_comments(review_id):
    sql = """
        SELECT comments.*, users.username
        FROM comments
        JOIN users ON comments.user_id = users.id
        WHERE comments.review_id = ?
        ORDER BY comments.id ASC
    """
    return db.query(sql, (review_id,))

def add_comment(review_id, user_id, comment):
    sql = """
        INSERT INTO comments (review_id, user_id, comment)
        VALUES (?, ?, ?)
    """
    db.execute(sql, (review_id, user_id, comment))

def delete_comment(comment_id):
    sql = """
        DELETE FROM comments
        WHERE id = ?
    """
    db.execute(sql, (comment_id,))

def get_comment(comment_id):
    sql = """
        SELECT *
        FROM comments
        WHERE id = ?
    """
    return db.query_one(sql, (comment_id,))