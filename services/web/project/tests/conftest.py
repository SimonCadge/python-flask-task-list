import pytest
from project import app, db

# Creates a test client and an app context that the tests can use to
# interact with the DB.
@pytest.fixture()
def client():
    with app.test_client() as test_client:
        with app.app_context():
            db.drop_all()
            db.create_all()
            db.session.commit()

            # Any other prep goes here

            yield test_client

            # Any teardown goes here