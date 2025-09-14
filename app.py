import os
import sqlite3
import colorgram
from flask import Flask, render_template, request, redirect, url_for, g

# Configuration
DATABASE = 'database.db'
UPLOAD_FOLDER = 'static/uploads'

# File extensions supported
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'supersecretkey' # Replace with a real secret key

# Database Setup 
def get_db():
    """Opens a new database connection if there is none yet for the current application context."""
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'db'):
        g.db.close()


def init_db():
    """Initializes the database schema."""
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


# Command to initialize DB from command line: flask init-db
@app.cli.command('init-db')
def init_db_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')


# Helper Functions
def allowed_file(filename):
    """Checks if a file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_colors(image_path, num_colors=5):
    """Extracts dominant colors from an image and returns them as hex strings."""
    try:
        colors = colorgram.extract(image_path, num_colors)
        hex_colors = []
        for color in colors:
            # Build the hex string manually from the r, g, b values
            # This is compatible with colorgram.py version 1.2.0
            hex_code = f"#{color.rgb.r:02x}{color.rgb.g:02x}{color.rgb.b:02x}"
            hex_colors.append(hex_code)
        return hex_colors
    except Exception as e:
        # If extraction fails for any reason, print the error and return empty.
        print(f"Could not extract colors: {e}")
        return []

# Routes
@app.route('/')
def index():
    """Main page - displays all clothing items in the closet."""
    db = get_db()
    items = db.execute('SELECT * FROM clothing ORDER BY id DESC').fetchall()
    return render_template('index.html', items=items)


@app.route('/add', methods=['GET', 'POST'])
def add_item():
    """Page to add a new clothing item."""
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = file.filename
            # Ensure the upload folder exists
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
            
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Extract colors from the saved image
            colors_list = extract_colors(filepath)
            colors_str = ','.join(colors_list) # Store as comma-separated string

            category = request.form['category']
            style = request.form['style']

            db = get_db()
            db.execute(
                'INSERT INTO clothing (filename, category, style, colors) VALUES (?, ?, ?, ?)',
                (filename, category, style, colors_str)
            )
            db.commit()
            return redirect(url_for('index'))

    return render_template('add_item.html')


@app.route('/delete/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    """Deletes an item from the closet and its image file."""
    db = get_db()
    item = db.execute('SELECT * FROM clothing WHERE id = ?', (item_id,)).fetchone()
    if item:
        # Delete the image file from the server
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], item['filename'])
        if os.path.exists(filepath):
            os.remove(filepath)
        
        # Delete the record from the database
        db.execute('DELETE FROM clothing WHERE id = ?', (item_id,))
        db.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    # Create the uploads folder if it doesn't exist
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    # Initialize the database if it doesn't exist
    if not os.path.exists(DATABASE):
        init_db()
    app.run(debug=True)

