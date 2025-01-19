# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
def get_earthquake(id):
    earthquake = Earthquake.query.get(id)
    if earthquake:
        return jsonify(earthquake.serialize), 200
    else:
        return make_response(jsonify({'message': f'Earthquake with ID {id} not found.'}), 404)


@app.route('/earthquakes/magnitude/<float:magnitude>', methods=['GET'])
def get_earthquakes_by_magnitude(magnitude):
    """
    View that returns earthquakes with a magnitude greater than or equal to the given value.

    :param magnitude: float, the magnitude threshold
    :return: JSON response with count and list of earthquakes
    """
    try:
        earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
        earthquake_list = [
            {
                "id": eq.id,
                "location": eq.location,
                "magnitude": eq.magnitude,
                "year": eq.year
            } for eq in earthquakes
        ]
        
        response = {
            "count": len(earthquake_list),
            "earthquakes": earthquake_list
        }
        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(port=5555, debug=True)
