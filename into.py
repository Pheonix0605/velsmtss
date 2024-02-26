from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3

app = Flask(__name__)
app.config['DATABASE'] = 'inventory.db'

# Function to get the SQLite connection
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db

# Function to close the SQLite connection
@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# Initialize the SQLite database
def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS items (
                            id INTEGER PRIMARY KEY,
                            name TEXT,
                            description TEXT,
                            quantity INTEGER,
                            price REAL
                        )''')
        db.commit()

@app.route('/')
def index():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM items')
    items = cursor.fetchall()
    return render_template('index1.html', items=items)

@app.route('/add', methods=['POST'])
def add_item():
    id = int(request.form['id'])
    name = request.form['name']
    description = request.form['description']
    quantity = int(request.form['quantity'])
    price = float(request.form['price'])
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''INSERT INTO items (id,name, description, quantity, price)
                      VALUES (?,?, ?, ?, ?)''', (id,name, description, quantity, price))
    db.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True, port=8000)

