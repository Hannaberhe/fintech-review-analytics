"""Database setup and data insertion using SQLite."""
import pandas as pd
import sqlite3

def setup_database():
    conn = sqlite3.connect('data/bank_reviews.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS banks (
            bank_id INTEGER PRIMARY KEY AUTOINCREMENT,
            bank_name TEXT NOT NULL,
            app_name TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
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
        )
    ''')
    
    banks = [
        ('Commercial Bank of Ethiopia', 'CBE Mobile'),
        ('Dashen Bank', 'Dashen Super App'),
        ('Bank of Abyssinia', 'BoA Mobile')
    ]
    cursor.executemany('INSERT INTO banks (bank_name, app_name) VALUES (?, ?)', banks)
    conn.commit()
    print("Database and tables created!")
    return conn

def insert_reviews(conn):
    df = pd.read_csv('data/raw/reviews_with_sentiment.csv')
    
    bank_map = {
        'Commercial Bank of Ethiopia': 1,
        'Dashen Bank': 2,
        'Bank of Abyssinia': 3
    }
    df['bank_id'] = df['bank'].map(bank_map)
    
    for _, row in df.iterrows():
        conn.execute('''
            INSERT INTO reviews (bank_id, review_text, rating, review_date, 
                               sentiment_label, sentiment_score, identified_theme, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            row['bank_id'], row['review'], row['rating'], row['date'],
            row['sentiment_label'], row['sentiment_score'], row['theme'], row['source']
        ))
    
    conn.commit()
    print(f"Inserted {len(df)} reviews!")

def run_queries(conn):
    print("\n=== VERIFICATION ===")
    
    query1 = '''
        SELECT b.bank_name, COUNT(r.review_id) as count, 
               ROUND(AVG(r.rating), 2) as avg_rating
        FROM banks b
        LEFT JOIN reviews r ON b.bank_id = r.bank_id
        GROUP BY b.bank_name
    '''
    result = pd.read_sql(query1, conn)
    print("\nReviews per bank:")
    print(result)
    
    query2 = 'SELECT COUNT(*) as nulls FROM reviews WHERE review_text IS NULL OR rating IS NULL'
    result2 = pd.read_sql(query2, conn)
    print(f"\nNull values: {result2['nulls'][0]}")

def export_schema():
    schema = '''
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
'''
    with open('data/schema.sql', 'w') as f:
        f.write(schema)
    print("Schema exported!")

if __name__ == "__main__":
    conn = setup_database()
    insert_reviews(conn)
    run_queries(conn)
    export_schema()
    conn.close()
    print("\nDatabase setup complete!")
