
CREATE TABLE banks (
    bank_id INTEGER PRIMARY KEY AUTOINCREMENT,
    bank_name TEXT NOT NULL,
    app_name TEXT
);

CREATE TABLE reviews (
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    bank_id INTEGER,
    review_text TEXT,
    rating INTEGER,
    review_date TEXT,
    sentiment_label TEXT,
    sentiment_score REAL,
    identified_theme TEXT,
    source TEXT,
    FOREIGN KEY (bank_id) REFERENCES banks(bank_id)
);
