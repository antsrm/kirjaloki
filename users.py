from werkzeug.security import generate_password_hash, check_password_hash
import db

def create_user(username, password):
    password_hash = generate_password_hash(password)

    sql = """
        INSERT INTO users (username, password_hash)
        VALUES (?, ?)
    """
    db.execute(sql, (username, password_hash))

def get_user_by_username(username):
    sql = "SELECT * FROM users WHERE username = ?"
    return db.query_one(sql, (username,))

def check_login(username, password):
    user = get_user_by_username(username)

    if not user:
        return None

    if not check_password_hash(user["password_hash"], password):
        return None

    return user