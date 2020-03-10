from app import app, db, request, jsonify, generate_password_hash, jwt_required, create_access_token, get_jwt_identity
from app.models import User

@app.route('/')
def hello():
    return 'hello'    

@app.route('/adduser')
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
        