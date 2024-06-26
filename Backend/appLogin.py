from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
import sqlite3
import requests
import logging

# Initialize logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Setup Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User class for Flask-Login
class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

@login_manager.user_loader
def load_user(user_id):
    logging.debug(f'Loading user with ID: {user_id}')
    conn = sqlite3.connect('brewery_reviews.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, username FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    if user:
        logging.debug(f'User found: {user}')
        return User(id=user[0], username=user[1])
    logging.debug('User not found')
    return None

# Initialize the database
def init_db():
    conn = sqlite3.connect('brewery_reviews.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
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

init_db()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        logging.debug(f'Attempting login with username: {username}')
        conn = sqlite3.connect('brewery_reviews.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            logging.debug(f'Login successful for user ID: {user[0]}')
            login_user(User(id=user[0], username=username))
            return redirect(url_for('search'))
        else:
            logging.debug('Invalid credentials')
            flash('Invalid credentials')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        logging.debug(f'Attempting signup with username: {username}')
        conn = sqlite3.connect('brewery_reviews.db')
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            logging.debug('Signup successful')
            flash('Signup successful, please log in.')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            logging.debug('Username already exists')
            flash('Username already exists.')
        finally:
            conn.close()
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logging.debug(f'Logging out user: {current_user.username}')
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def search():
    return render_template('search.html')

@app.route('/search', methods=['GET'])
@login_required
def search_results():
    query = request.args.get('query')
    search_by = request.args.get('search_by')
    logging.debug(f'Searching breweries by {search_by} with query: {query}')
    
    if search_by == 'name':
        response = requests.get(f'https://api.openbrewerydb.org/breweries?by_name={query}')
    elif search_by == 'city':
        response = requests.get(f'https://api.openbrewerydb.org/breweries?by_city={query}')
    elif search_by == 'type':
        response = requests.get(f'https://api.openbrewerydb.org/breweries?by_type={query}')
    else:
        response = []

    breweries = response.json() if response.status_code == 200 else []
    logging.debug(f'Found breweries: {breweries}')
    return render_template('search_results.html', breweries=breweries)

@app.route('/brewery/<int:brewery_id>')
@login_required
def brewery(brewery_id):
    logging.debug(f'Fetching details for brewery ID: {brewery_id}')
    conn = sqlite3.connect('brewery_reviews.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM breweries WHERE id = ?', (brewery_id,))
    brewery = cursor.fetchone()
    cursor.execute('SELECT * FROM reviews WHERE brewery_id = ?', (brewery_id,))
    reviews = cursor.fetchall()
    conn.close()
    logging.debug(f'Brewery details: {brewery}')
    logging.debug(f'Reviews: {reviews}')
    return render_template('brewery.html', brewery=brewery, reviews=reviews)

@app.route('/add_review/<int:brewery_id>', methods=['POST'])
@login_required
def add_review(brewery_id):
    rating = request.form['rating']
    description = request.form['description']
    logging.debug(f'Adding review for brewery ID: {brewery_id}, rating: {rating}, description: {description}')
    conn = sqlite3.connect('brewery_reviews.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO reviews (brewery_id, rating, description) VALUES (?, ?, ?)',
                   (brewery_id, rating, description))
    conn.commit()
    conn.close()
    return redirect(url_for('brewery', brewery_id=brewery_id))

if __name__ == '__main__':
    app.run(debug=True)
