import os
import json
from flask import Flask, render_template, request, jsonify
import verification_code_generator

app = Flask(__name__)

# Ensure config.json is loaded if not already handled by the library
if not os.environ.get("VERICODE_SECRET_KEY"):
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
            os.environ["VERICODE_SECRET_KEY"] = config.get("VERICODE_SECRET_KEY")
    except Exception as e:
        print(f"Warning: Could not load config.json: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    try:
        code = verification_code_generator.generate_code(user_id)
        return jsonify({'code': code})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/validate', methods=['POST'])
def validate():
    data = request.get_json()
    user_id = data.get('user_id')
    code = data.get('code')

    if not user_id or not code:
        return jsonify({'error': 'User ID and Code are required'}), 400

    try:
        is_valid = verification_code_generator.validate_code(code, user_id)
        return jsonify({'valid': is_valid})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
