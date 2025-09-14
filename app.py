from dotenv import load_dotenv
import os
from supabase import create_client, Client
from flask import Flask, request, jsonify
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

app = Flask(__name__)

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

    # Store in Supabase
    calc_data = {
        'expression': expression,
        'result': result,
        'timestamp': datetime.utcnow().isoformat()  # ISO format for Supabase
    }
    try:
        supabase.table('calculations').insert(calc_data).execute()
    except Exception as e:
        return jsonify({'error': 'Failed to save calculation'}), 500

    # Get all past calculations from Supabase
    try:
        response = supabase.table('calculations').select('*').order('timestamp', desc=True).execute()
        past_calcs = response.data  # Supabase returns data in 'data' key
        calc_list = [
            {
                'expression': c['expression'],
                'result': c['result'],
                'timestamp': c['timestamp']
            } for c in past_calcs
        ]
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve calculations'}), 500

    return jsonify({'result': result, 'past_calculations': calc_list})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)