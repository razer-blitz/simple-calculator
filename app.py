from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# Configure SQLite database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'calculations.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database model for storing calculations
class Calculation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    expression = db.Column(db.String(100), nullable=False)
    result = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Create database tables
with app.app_context():
    db.create_all()

# Route to serve the frontend
@app.route('/')
def index():
    return app.send_static_file('index.html')

# Route to handle calculation
@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    expression = data.get('expression')
    
    try:
        # Evaluate the expression (basic math only for learning)
        result = str(eval(expression))  # Warning: eval() is unsafe in production!
    except Exception as e:
        return jsonify({'error': 'Invalid expression'}), 400
    
    # Store in database
    calc = Calculation(expression=expression, result=result)
    db.session.add(calc)
    db.session.commit()
    
    # Get all past calculations
    past_calcs = Calculation.query.order_by(Calculation.timestamp.desc()).all()
    calc_list = [
        {
            'expression': c.expression,
            'result': c.result,
            'timestamp': c.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        } for c in past_calcs
    ]
    
    return jsonify({'result': result, 'past_calculations': calc_list})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True) #  For local-  app.run(debug=True)