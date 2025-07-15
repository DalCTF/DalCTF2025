from flask import Flask, render_template, jsonify, request, redirect, url_for, make_response
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, set_access_cookies, unset_jwt_cookies
from datetime import timedelta
import os
from dotenv import load_dotenv
from functools import wraps
import jwt as PyJWT  # PyJWT package but module name is 'jwt'
import random
import string

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure Flask-JWT-Extended
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', os.urandom(64).hex())  # 64 bytes random string as default
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_SECURE'] = False #os.getenv('FLASK_ENV') == 'production'  # True in production
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
app.config['JWT_COOKIE_SAMESITE'] = 'Strict'
jwt = JWTManager(app)

def generate_letter_grid(hidden_phrase):
    COLS = 30
    ROWS = 20

    # Initialize 20x20 grid with spaces
    grid = [[' ' for _ in range(COLS)] for _ in range(ROWS)]
    
    # Place the hidden phrase horizontally in a random position
    phrase = hidden_phrase.upper()
    if len(phrase) > COLS:
        phrase = phrase[:COLS]  # Truncate if too long
    
    # Choose random starting position that ensures phrase fits
    start_row = random.randint(0, ROWS-1)
    start_col = random.randint(0, COLS - len(phrase))
    
    # Place the phrase
    phrase_positions = sorted(random.sample(range(0, COLS * ROWS), len(phrase)))

    for i, letter in enumerate(phrase):
        row = phrase_positions[i] // COLS
        col = phrase_positions[i] % COLS
        if letter != ' ':
            grid[row][col] = { 'letter': letter, 'class': 'g' }
    
    # Fill remaining spaces with random letters
    for i in range(ROWS):
        for j in range(COLS):
            if grid[i][j] == ' ':
                grid[i][j] = { 'letter': random.choice(string.ascii_uppercase), 'class': 'q' }
    
    return grid

def jwt_username_only(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        jwt_token = request.cookies.get('access_token_cookie')
        if not jwt_token:
            return redirect(url_for('home'))
        
        try:
            # Decode without verification
            decoded_token = PyJWT.decode(jwt_token, options={"verify_signature": False})
            username = decoded_token.get('sub')  # JWT standard uses 'sub' for subject/username
            if not username:
                return redirect(url_for('home'))
            return view_function(username=username, *args, **kwargs)
        except PyJWT.InvalidTokenError:
            return redirect(url_for('home'))
    
    return decorated_function

# Simulated user database (replace with real database in production)
USERS = {
    'admin': 'password123'  # In production, use hashed passwords!
}

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/dashboard')
@jwt_username_only
def dashboard(username):
    # Generate grid with a hidden message
    hidden_phrase = "GUESTS ARE NOT admin"
    if username == 'admin':
        hidden_phrase = "dalctf{why_d0_w3_3v3n_h4v3_jwts?}"

    letter_grid = generate_letter_grid(hidden_phrase)
    return render_template('dashboard.html', username=username, grid=letter_grid)

@app.route('/api/auth/login', methods=['POST'])
def login():
    # We will always fail the login
    # But that's on purpose
    return jsonify({"msg": "Bad username or password"}), 401

    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400

    if USERS.get(username) != password:
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    response = jsonify({"msg": "Login successful"})
    set_access_cookies(response, access_token)
    return response

@app.route('/api/auth/guest', methods=['POST'])
def guest_login():
    access_token = create_access_token(identity="guest")
    response = jsonify({"msg": "Guest login successful"})
    set_access_cookies(response, access_token)
    return response

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    response = jsonify({"msg": "Logout successful"})
    unset_jwt_cookies(response)
    return response

if __name__ == '__main__':
    app.run(debug=True) 
