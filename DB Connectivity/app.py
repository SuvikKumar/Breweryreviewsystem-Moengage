from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('brewery_reviews.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS breweries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location TEXT NOT NULL,
            description TEXT NOT NULL
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

init_db()

@app.route('/')
def index():
    conn = sqlite3.connect('brewery_reviews.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM breweries')
    breweries = cursor.fetchall()
    conn.close()
    return render_template('index.html', breweries=breweries)

@app.route('/brewery/<int:brewery_id>')
def brewery(brewery_id):
    conn = sqlite3.connect('brewery_reviews.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM breweries WHERE id = ?', (brewery_id,))
    brewery = cursor.fetchone()
    cursor.execute('SELECT * FROM reviews WHERE brewery_id = ?', (brewery_id,))
    reviews = cursor.fetchall()
    conn.close()
    return render_template('brewery.html', brewery=brewery, reviews=reviews)

@app.route('/add_review/<int:brewery_id>', methods=['POST'])
def add_review(brewery_id):
    rating = request.form['rating']
    description = request.form['description']
    conn = sqlite3.connect('brewery_reviews.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO reviews (brewery_id, rating, description) VALUES (?, ?, ?)',
                   (brewery_id, rating, description))
    conn.commit()
    conn.close()
    return redirect(url_for('brewery', brewery_id=brewery_id))

if __name__ == '__main__':
    app.run(debug=True)
