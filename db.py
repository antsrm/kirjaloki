import sqlite3

DATABASE = "database.db"

def get_connection():
    con = sqlite3.connect(DATABASE)
    con.row_factory = sqlite3.Row
    return con

def execute(sql, params=()):
    con = get_connection()
    result = con.execute(sql, params)
    con.commit()
    con.close()
    return result

def query(sql, params=()):
    con = get_connection()
    result = con.execute(sql, params).fetchall()
    con.close()
    return result

def query_one(sql, params=()):
    con = get_connection()
    result = con.execute(sql, params).fetchone()
    con.close()
    return result