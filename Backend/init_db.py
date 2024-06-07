def init_db():
    conn = sqlite3.connect('brewery_reviews.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS breweries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location TEXT NOT NULL,
            address TEXT NOT NULL,
            phone TEXT,
            website TEXT,
            city TEXT,
            state TEXT,
            type TEXT,
            current_rating REAL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brewery_id INTEGER,
            rating INTEGER NOT NULL,
            description TEXT NOT NULL,
            FOREIGN KEY (brewery_id) REFERENCES breweries(id)
        )
    ''')
    conn.commit()
    conn.close()
