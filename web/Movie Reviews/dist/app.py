from flask_jwt_extended import JWTManager, create_access_token, set_access_cookies, unset_jwt_cookies
from flask import Flask, render_template, jsonify, request, redirect, url_for, send_from_directory, make_response
from datetime import timedelta
from functools import wraps
import jwt as PyJWT
import os
import psycopg2
import hashlib
import uuid

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', os.urandom(64).hex())
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
app.config['JWT_COOKIE_SAMESITE'] = 'Strict'
app.config['JWT_COOKIE_SECURE'] = False
jwt = JWTManager(app)



def jwt_protect(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        jwt_token = request.cookies.get('access_token_cookie')
        if not jwt_token:
            return redirect(url_for('home'))
        
        try:
            secret_key = app.config['JWT_SECRET_KEY']
            decoded_token = PyJWT.decode(jwt_token, secret_key, algorithms=["HS256"])
            username = decoded_token.get('sub')
            if not username:
                return redirect(url_for('home'))
            return view_function(username=username, *args, **kwargs)
        except PyJWT.InvalidTokenError:
            return redirect(url_for('home'))
    
    return decorated_function

def get_db_conn():
    try:
        return psycopg2.connect(
            password=os.getenv('POSTGRES_PASSWORD'),
            database=os.getenv('POSTGRES_DB'),
            host=os.getenv('POSTGRES_HOST'),
            user=os.getenv('POSTGRES_USER'),
            port=os.getenv('POSTGRES_PORT'),
        )
    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
        return None

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def db_error_response(error_msg="Database error"):
    return jsonify({"msg": error_msg}), 500

def ensure_unique_cookie(response=None):
    if response is None:
        response = make_response()
    
    if 'unique' not in request.cookies:
        unique_id = str(uuid.uuid4())
        response.set_cookie('unique', unique_id, max_age=31536000, httponly=True, samesite='Strict')
    
    return response

@app.route('/')
def home():
    response = make_response(render_template('login.html'))
    return ensure_unique_cookie(response)

@app.route('/register')
def register_page():
    response = make_response(render_template('register.html'))
    return ensure_unique_cookie(response)

@app.route('/dashboard')
@jwt_protect
def dashboard(username):
    conn = get_db_conn()
    if not conn:
        response = make_response(render_template('dashboard.html', username=username, reviews=[], movies=[], error="Database connection error"))
        return ensure_unique_cookie(response)

    try:
        cursor = conn.cursor()
        
        cursor.execute("SELECT title, director, release_year, genre FROM movies ORDER BY title")
        movies = [{'title': m[0], 'director': m[1], 'release_year': m[2], 'genre': m[3]} for m in cursor.fetchall()]
        
        unique_id = request.cookies.get('unique')
        
        query = f"SELECT m.title, m.director, m.release_year, m.genre, m.poster_url, r.rating, r.review_text, r.created_at FROM reviews r JOIN movies m ON r.movie_id = m.id WHERE (r.unique_id = '{unique_id}' OR r.unique_id IS NULL) AND (r.username = '{username}') ORDER BY r.created_at DESC"
        cursor.execute(query)
        
        reviews = [{
            'title': r[0], 'director': r[1], 'release_year': r[2], 'genre': r[3],
            'poster_url': r[4], 'rating': r[5], 'review_text': r[6], 'created_at': r[7]
        } for r in cursor.fetchall()]
        
        response = make_response(render_template('dashboard.html', username=username, reviews=reviews, movies=movies))
        return ensure_unique_cookie(response)
        
    except psycopg2.Error as e:
        print(f"Database error: {e}")
        response = make_response(render_template('dashboard.html', username=username, reviews=[], movies=[], error="Database error"))
        return ensure_unique_cookie(response)
    finally:
        conn.close()

@app.route('/api/auth/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        response = jsonify({"msg": "Missing username or password"}), 400
        return ensure_unique_cookie(response[0]), response[1]

    unique_id = request.cookies.get('unique')
    if not unique_id:
        response = jsonify({"msg": "Unique identifier not found"}), 400
        return ensure_unique_cookie(response[0]), response[1]

    conn = get_db_conn()
    if not conn:
        response = db_error_response("Database connection error")
        return ensure_unique_cookie(response[0]), response[1]

    try:
        cursor = conn.cursor()
        password_hash = hash_password(password)
        
        cursor.execute("SELECT username FROM users WHERE username = %s AND unique_id = %s", (username, unique_id))
        if cursor.fetchone():
            response = jsonify({"msg": "Username already exists"}), 409
            return ensure_unique_cookie(response[0]), response[1]

        cursor.execute("INSERT INTO users (username, password_hash, unique_id) VALUES (%s, %s, %s)", (username, password_hash, unique_id))
        conn.commit()
        response = jsonify({"msg": "Registration successful"}), 201
        return ensure_unique_cookie(response[0]), response[1]
        
    except psycopg2.Error as e:
        print(f"Database error: {e}")
        conn.rollback()
        response = db_error_response()
        return ensure_unique_cookie(response[0]), response[1]
    finally:
        conn.close()

@app.route('/api/auth/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        response = jsonify({"msg": "Missing username or password"}), 400
        return ensure_unique_cookie(response[0]), response[1]

    unique_id = request.cookies.get('unique')
    if not unique_id:
        response = jsonify({"msg": "Unique identifier not found"}), 400
        return ensure_unique_cookie(response[0]), response[1]

    conn = get_db_conn()
    if not conn:
        response = db_error_response("Database connection error")
        return ensure_unique_cookie(response[0]), response[1]

    try:
        cursor = conn.cursor()
        password_hash = hash_password(password)
        
        cursor.execute("SELECT username FROM users WHERE username = %s AND password_hash = %s AND unique_id = %s", (username, password_hash, unique_id))
        if not cursor.fetchone():
            response = jsonify({"msg": "Bad username or password"}), 401
            return ensure_unique_cookie(response[0]), response[1]

        access_token = create_access_token(identity=username)
        response = jsonify({"msg": "Login successful"})
        set_access_cookies(response, access_token)
        return ensure_unique_cookie(response)
        
    except psycopg2.Error as e:
        print(f"Database error: {e}")
        response = db_error_response()
        return ensure_unique_cookie(response[0]), response[1]
    finally:
        conn.close()

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    response = jsonify({"msg": "Logout successful"})
    unset_jwt_cookies(response)
    return ensure_unique_cookie(response)

@app.route('/api/reviews/add', methods=['POST'])
@jwt_protect
def add_review(username):
    movie_title = request.json.get('movie_title')
    rating = request.json.get('rating')
    review_text = request.json.get('review_text')

    if not movie_title or not rating or not review_text:
        response = jsonify({"msg": "Missing required fields"}), 400
        return ensure_unique_cookie(response[0]), response[1]

    if not isinstance(rating, int) or rating < 1 or rating > 10:
        response = jsonify({"msg": "Rating must be an integer between 1 and 10"}), 400
        return ensure_unique_cookie(response[0]), response[1]

    conn = get_db_conn()
    if not conn:
        response = db_error_response("Database connection error")
        return ensure_unique_cookie(response[0]), response[1]

    try:
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM movies WHERE title = %s", (movie_title,))
        movie = cursor.fetchone()
        if not movie:
            response = jsonify({"msg": "Movie not found"}), 404
            return ensure_unique_cookie(response[0]), response[1]

        unique_id = request.cookies.get('unique')
        
        cursor.execute("""
            INSERT INTO reviews (username, movie_id, unique_id, rating, review_text)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (username, movie_id, unique_id) 
            DO UPDATE SET rating = EXCLUDED.rating, review_text = EXCLUDED.review_text, created_at = CURRENT_TIMESTAMP
        """, (username, movie[0], unique_id, rating, review_text))
        
        conn.commit()
        response = jsonify({"msg": "Review submitted successfully"}), 201
        return ensure_unique_cookie(response[0]), response[1]
        
    except psycopg2.Error as e:
        print(f"Database error: {e}")
        conn.rollback()
        response = db_error_response()
        return ensure_unique_cookie(response[0]), response[1]
    finally:
        conn.close()

@app.route('/static/posters/<filename>')
def serve_poster(filename):
    response = make_response(send_from_directory('public', filename))
    return ensure_unique_cookie(response)

if __name__ == '__main__':
    app.run()
