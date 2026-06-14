CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE reviews (
    id INTEGER PRIMARY KEY,
    title TEXT,
    author TEXT,
    rating INTEGER,
    review TEXT,
    user_id INTEGER REFERENCES users(id)
);

CREATE TABLE genres (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE review_genres (
    review_id INTEGER REFERENCES reviews(id),
    genre_id INTEGER REFERENCES genres(id),
    PRIMARY KEY (review_id, genre_id)
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    review_id INTEGER REFERENCES reviews(id),
    user_id INTEGER REFERENCES users(id),
    comment TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);