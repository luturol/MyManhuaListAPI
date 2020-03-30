import os
import tempfile
from flask import Flask, Response as BaseResponse, json
import pytest

from app import app, db, migrate

@pytest.fixture
def client():    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(__file__), 'test.db')
    app.config['TESTING'] = True
    db.init_app(app)
    with app.app_context():
        db.create_all()     
        migrate.init_app(app, db)
    
    with app.test_client() as client:       
        yield client
        print("Teardown context")
        db.session.remove()
        db.drop_all()
        os.remove(os.path.join(os.path.dirname(__file__), 'test.db'))    
    
def test_hello(client):
    response = client.get('/')
    print(response.get_data())
    assert b'hello' in response.get_data()

def test_add_user(client):
    response = client.post('/adduser', data=json.dumps(dict(
        username = 'rafael',
        password = '1234',
        email = 'rafael.ahrons@gmail.com'
    )), content_type='application/json', follow_redirects=True)

    print(response.data)

    assert b'User saved with success' in response.get_data()