from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__, static_folder='../static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:testpass@localhost/app_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Models
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    time = db.Column(db.Integer, nullable=False, default=0)

# Routes
@app.route('/categories', methods=['GET', 'POST'])
def manage_categories():
    try:
        if request.method == 'POST':
            # Handle adding a new category
            data = request.get_json()
            new_category = Category(name=data['name'], time=0)
            db.session.add(new_category)
            db.session.commit()
            return jsonify({'id': new_category.id, 'name': new_category.name, 'time': new_category.time}), 201
        else:
            # Handle fetching all categories
            categories = Category.query.all()
            if not categories:  # Debug log for empty table
                print("No categories found in the database.")
            return jsonify([{'id': c.id, 'name': c.name, 'time': c.time} for c in categories])
    except Exception as e:
        print("Error in /categories route:", str(e))  # Log the error for debugging
        return jsonify({'error': 'Internal Server Error'}), 500


@app.route('/categories/<int:category_id>', methods=['POST'])
def update_category_time(category_id):
    try:
        data = request.get_json()
        time_change = data.get('time', 0)

        category = Category.query.get(category_id)
        if not category:
            return jsonify({'error': 'Category not found'}), 404

        # Ensure time doesn't go below zero
        new_time = category.time + time_change
        if new_time < 0:
            new_time = 0

        category.time = new_time
        db.session.commit()

        return jsonify({'id': category.id, 'name': category.name, 'time': category.time})
    except Exception as e:
        print("Error in /categories/<int:category_id> route:", str(e))
        return jsonify({'error': str(e)}), 500


@app.route('/seed', methods=['POST'])
def seed_data():
    try:
        category1 = Category(name="Reading", time=5)
        category2 = Category(name="Exercise", time=3)
        db.session.add_all([category1, category2])
        db.session.commit()
        return jsonify({"message": "Seeded categories!"}), 201
    except Exception as e:
        print("Error in /seed route:", str(e))
        return jsonify({'error': 'Internal Server Error'}), 500


# Frontend Route
@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

from sqlalchemy.sql import text

try:
    with app.app_context():
        db.session.execute(text('SELECT 1'))
        print("Database connection successful.")
except Exception as e:
    print("Database connection error:", str(e))

if __name__ == "__main__":
    app.run(debug=True, port=8000)