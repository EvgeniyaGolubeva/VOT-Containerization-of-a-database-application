from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import os
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__, static_folder='../static')

# Enable CORS for all routes
CORS(app)

# Database configuration
#app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
#    'SQLALCHEMY_DATABASE_URI',
#    'mysql+pymysql://root:testpass@db/app_db'  # Fallback for local testing
#)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:testpass@db/app_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Models
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    time = db.Column(db.Integer, nullable=False, default=0)

# Routes
@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>', methods=['GET'])
def serve_static_files(path):
    return send_from_directory(app.static_folder, path)

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
            return jsonify([{'id': c.id, 'name': c.name, 'time': c.time} for c in categories])
    except Exception as e:
        print("Error in /categories route:", str(e))
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

from sqlalchemy.sql import text

with app.app_context():
    db.create_all()



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
