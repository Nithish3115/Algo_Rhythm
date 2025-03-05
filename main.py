import os
import logging
from flask import Flask, render_template, request, jsonify
from melody_generator import generate_melody

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default_secret_key")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        username = request.form.get('username', '').strip()
        if not username:
            return jsonify({'error': 'Please enter a username'}), 400
           
        # Generate melody data
        melody_data = generate_melody(username)
        return jsonify({'melody': melody_data})
       
    except Exception as e:
        logging.error(f"Error generating melody: {str(e)}")
        return jsonify({'error': 'Failed to generate melody'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

