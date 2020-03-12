from app import app, db, request, jsonify, generate_password_hash, jwt_required, create_access_token, get_jwt_identity, check_password_hash, Config
from app.models import User
import requests
from flask_cors import cross_origin

@app.route('/')
@cross_origin()
def hello():
    return 'hello'    

@app.route('/login', methods=['POST'])
@cross_origin()
def login():
    try:
        if not request.is_json:
            raise Exception("Request must be in json format")

        user_login = request.get_json()
        if 'username' not in user_login or 'password' not in user_login:
            raise Exception("Request must have all the required fields")
        
        user = User.query.filter(User.username == user_login['username'] or User.email == user_login['username']).first()        
        if not user or not check_password_hash(user.password, user_login['password']):
            raise Exception('Invalid username or password')
        
        response = jsonify({'msg': 'User logged with success', 'token': create_access_token(identity=user_login['username'])})
        response.status_code = 200
        
        return response
    except Exception as error:
        response = jsonify("{0}".format(str(error)))
        response.status_code = 400
        return response
    

@app.route('/adduser', methods=['POST'])
def add_user():
    try:
        if not request.is_json:
            raise Exception('Request must be in json format')

        username = request.json.get('username')
        password = request.json.get('password')
        email = request.json.get('email')
        
        if not username or not password or not email:
            raise Exception('Request must contain all required fields.')
        
        user_exist = User.query.filter(User.username == username).first() is not None
        if user_exist:
            raise Exception("User already exist")

        email_has_user = User.query.filter(User.email == email).first() is not None
        if email_has_user:
            raise Exception("E-mail already has a user")
        
        password_hash = generate_password_hash(password)
        db.session.add(User(username=username, email=email, password=password_hash))
        db.session.commit()

        response = jsonify("User saved with success")
        response.status_code = 200
        send_simple_message(email)

        return response
    except Exception as error:
        response = jsonify("{0}".format(str(error)))
        response.status_code = 400
        return response

def send_simple_message(email):    
    domain = Config.MAILGUN_API_DOMAIN
    email_sender = Config.MAILGUN_EMAIL_SENDER
    api_key = Config.MAILGUN_API_KEY

    return requests.post("https://api.mailgun.net/v3/{}/messages".format(domain), 
            auth=("api", api_key), 
            data={"from": email_sender, 
             "to": [email], 
             "subject": "Hello", 
             "text": "Testing some Mailgun awesomness!"})