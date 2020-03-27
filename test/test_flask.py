import os
import tempfile

import pytest

from app import app

@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True

    with app.app.test_client() as client:
        with app.app.context():
            app.init_db()
        yield client
    
    os.close(db_fd)
    os.unlink(app.app.config['DATABASE'])
    