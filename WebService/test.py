import flask_unittest
import unittest
import json
from Models.events import Events, EventsSchema
from app import create_app
from Models.shared import db

class FlaskTest(flask_unittest.ClientTestCase):
    # Assign the flask app object
    app = create_app()
    app.config["TESTING"] = True
    app.testing = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

    def setUp(self, client):
        ctx = self.app.test_request_context()
        ctx.push()
        db.create_all()
        event1 = Events(classes="[bird, chicken]", video="VIDEOS3KEY", access_granted=True)
        db.session.add(event1)
        db.session.commit()
        ctx.pop()

    # Check for response 200
    def test_health_check(self, client):
        response = client.get("/health_check")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    # Check if context of index is application/html
    def test_index_content(self, client):
        response = client.get("/")
        self.assertEqual(response.content_type, "text/html; charset=utf-8")

    # Check if GET events returns the element that we entered in setup
    def test_get_events(self, client):
        response = client.get("/events")
        json_response = json.loads(response.get_data(as_text=True))
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertTrue(
            any(
                e['access_granted'] == True and
                e['id'] == 1 and
                e["classes"] == '[bird, chicken]' and
                e['video'] == 'VIDEOS3KEY'
                for e in json_response
            )
        )

    # Check if object entered in POST events is stored in database
    def test_post_events(self, client):
        response = client.post("/events",
                               data=json.dumps(dict(classes='[dog, cat]', video='TESTPOST', access_granted=True)),
                               content_type='application/json')
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

        response = client.get("/events")
        json_response = json.loads(response.get_data(as_text=True))
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertTrue(
            any(
                e['access_granted'] == True and
                e["classes"] == '[dog, cat]' and
                e['video'] == 'TESTPOST'
                for e in json_response
            )
        )

if __name__ =="__main__":
    unittest.main()