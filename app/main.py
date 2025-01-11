# from flask import Flask, request, jsonify
# from database import initialize_db, fetch_data, insert_new_data

# app = Flask(__name__)

# initialize_db()

# @app.route('/predict', methods=['POST'])
# def predict():
#     input_data = request.get_json()
#     # Here, you'd include your model prediction logic
#     return jsonify({"prediction": "Example Prediction"})

# @app.route('/data', methods=['GET'])
# def get_data():
#     rows = fetch_data()
#     return jsonify(rows)

# @app.route('/data', methods=['POST'])
# def add_data():
#     new_data = request.get_json()
#     insert_new_data(new_data)
#     return jsonify({"status": "success"}), 201

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0')



from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database URI (use your own credentials)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/real_estate'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the model for the apartments table
class Apartment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    district = db.Column(db.String(255))
    price = db.Column(db.Numeric)
    price_per_sqm = db.Column(db.Numeric)
    currency = db.Column(db.String(3))
    apartment_type = db.Column(db.String(255))
    date = db.Column(db.Date)

@app.route('/')
def index():
    # Query data from the database
    apartments = Apartment.query.all()
    return render_template('index.html', apartments=apartments)

if __name__ == '__main__':
    app.run(debug=True)
