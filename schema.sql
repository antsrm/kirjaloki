CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE reviews (
    id INTEGER PRIMARY KEY,
    title TEXT,
    author TEXT,
    rating INTEGER,
    review TEXT,
    user_id INTEGER REFERENCES users(id)
);