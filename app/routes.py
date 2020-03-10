from app import app, db, request, jsonify, generate_password_hash, jwt_required, create_access_token, get_jwt_identity, check_password_hash
from app.models import User

@app.route('/')
def hello():
    return 'hello'    

@app.route('/login', methods=['GET'])
def login():
    try:
        if not request.is_json:
            raise Exception("Request must be in json format")

        user_login = request.get_json()
        if 'username' not in user_login or 'password' not in user_login:
            raise Exception("Request must have all the required fields")
        
        user = User.query.filter(User.username == user_login['username']).first()
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
@jwt_required
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

        return response
    except Exception as error:
        response = jsonify("{0}".format(str(error)))
        response.status_code = 400
        return response
        