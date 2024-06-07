@app.route('/search')
@login_required
def search():
    query = request.args.get('query')
    search_by = request.args.get('search_by')
    conn = sqlite3.connect('brewery_reviews.db')
    cursor = conn.cursor()

    if search_by == 'name':
        cursor.execute('SELECT * FROM breweries WHERE name LIKE ?', ('%' + query + '%',))
    elif search_by == 'city':
        cursor.execute('SELECT * FROM breweries WHERE location LIKE ?', ('%' + query + '%',))
    elif search_by == 'type':
        cursor.execute('SELECT * FROM breweries WHERE type LIKE ?', ('%' + query + '%',))  # Assuming there is a 'type' column

    breweries = cursor.fetchall()
    conn.close()
    return render_template('search_results.html', breweries=breweries)
