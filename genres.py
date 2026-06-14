import db

def get_genres():
    sql = """
        SELECT *
        FROM genres
        ORDER BY name
    """
    return db.query(sql)

def get_review_genres(review_id):
    sql = """
        SELECT genres.*
        FROM genres
        JOIN review_genres
            ON genres.id = review_genres.genre_id
        WHERE review_genres.review_id = ?
        ORDER BY genres.name
    """
    return db.query(sql, (review_id,))

def add_review_genres(review_id, genre_ids):
    sql = """
        INSERT OR IGNORE INTO review_genres (review_id, genre_id)
        VALUES (?, ?)
    """

    for genre_id in genre_ids:
        db.execute(sql, (review_id, genre_id))

def delete_review_genres(review_id):
    sql = """
        DELETE FROM review_genres
        WHERE review_id = ?
    """

    db.execute(sql, (review_id,))

def get_review_genre_names(review_id):
    sql = """
        SELECT genres.name
        FROM genres
        JOIN review_genres
            ON genres.id = review_genres.genre_id
        WHERE review_genres.review_id = ?
        ORDER BY genres.name
    """
    return db.query(sql, (review_id,))