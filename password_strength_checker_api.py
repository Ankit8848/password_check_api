from flask import Flask, request, jsonify
import re
import os

app = Flask(__name__)


def is_strong_password(password):
    # Define basic rules for a strong password
    # At least 8 characters
    # At least one uppercase letter
    # At least one lowercase letter
    # At least one digit
    # At least one special character (e.g., @, #, $, %, etc.)
    if (
            len(password) >= 8 and
            re.search(r'[A-Z]', password) and
            re.search(r'[a-z]', password) and
            re.search(r'[0-9]', password) and
            re.search(r'[!@#$%^&*()_+{}\[\]:;<>,.?~\\-]', password)
    ):
        return True
    return False


@app.route('/check_password', methods=['POST'])
def check_password_strength():
    try:
        # Get the password from the request JSON data
        data = request.get_json()
        password = data.get('password')

        if not password:
            return jsonify({'error': 'Missing password in request JSON'}), 400

        # Check if the password is strong or weak
        if is_strong_password(password):
            strength = 'Strong'
        else:
            strength = 'Weak'

        # Prepare the response JSON object
        response_data = {
            'password': password,
            'strength': strength
        }

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=True)
