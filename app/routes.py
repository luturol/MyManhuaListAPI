from app import app, db, request, jsonify, generate_password_hash, jwt_required, create_access_token, get_jwt_identity, check_password_hash, Config
from app.models import User, Manga
import requests
from flask_cors import cross_origin
from sqlalchemy import or_
from datetime import datetime, timedelta

@app.route('/')
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

        user = User.query.filter(or_(User.username == user_login['username'], User.email == user_login['username'])).first()        
        if not user or not check_password_hash(user.password, user_login['password']):
            raise Exception('Invalid username or password')
                
        response = jsonify({'msg': 'User logged with success', 
                            'token': create_access_token(identity=user.username),
                            'expiration_date': (datetime.now() + Config.JWT_ACCESS_TOKEN_EXPIRES).strftime("%d/%m/%Y %H:%M:%S") })
        response.status_code = 200
        
        return response
    except Exception as error:
        response = jsonify({ 'msg': "{0}".format(str(error)), 'error': True})
        response.status_code = 400
        return response
    

@app.route('/adduser', methods=['POST'])
@cross_origin()
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

        response = jsonify({ 'msg': "User saved with success" })
        response.status_code = 200
        send_simple_message(email)

        return response
    except Exception as error:
        response = jsonify({ 'msg': "{0}".format(str(error)), 'error': True })
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

@app.route('/addmanga', methods=['POST'])
@cross_origin()
@jwt_required
def add_manga():
    try:
        if not request.is_json:
            raise Exception('Request must be in json format')
        
        manga = request.get_json()
        if 'name' not in manga or 'chapter' not in manga or 'status' not in manga:
            raise Exception('Need to send all required fields for the request')
        
        if not manga['name'] or not manga['chapter'] or not manga['status']:
            raise Exception('Need to fill all required fields for the request')

        username = get_jwt_identity()

        db.session.add(Manga(user_id=username, name=manga['name'], chapter=manga['chapter'], state=manga['state']))
        db.session.commit()

        response = jsonify({ 'msg': 'Manga added with success'})
        response.status_code = 200

        return response        
    except Exception as error:
        response = jsonify({ 'msg': "{0}".format(str(error)), 'error': True })
        response.status_code = 400
        return response

@app.route('/getmangas', methods=['GET'])
@cross_origin()
@jwt_required
def get_mangas():
    try:
        username = get_jwt_identity()
        mangas = Manga.query.filter(Manga.username == username).all()

        response = jsonify({ 'mangas': mangas })
        response.status_code = 200
        
        return response
    except Exception as error:
        response = jsonify({ 'msg': "{0}".format(str(error)), 'error': True })
        response.status_code = 400
        return response