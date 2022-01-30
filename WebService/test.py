import flask_unittest
import unittest
import json
from Models.events import Events, EventsSchema
from app import create_app
from Models.shared import db
from camera import Video

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

    # Provided a video of a cat, the Video class should be able to detect a cat
    def test_detect_cat(self, client):
        camera = Video(cameraSource="test_videos/cat.mp4", timeout=0)
        response = camera.get_frame()
        labels = response['labels']
        self.assertTrue('cat' in labels)
        self.assertTrue('cat_mouth' in labels)
        self.assertTrue('cat_eye' in labels)
        self.assertTrue('cat_nose' in labels)

    # Provided a video of a mailing package, the Video class should detect a package, person, but not cats
    def test_detect_package(self, client):
        camera = Video(cameraSource="test_videos/package.mp4", timeout=0)
        response = camera.get_frame()
        labels = response['labels']
        self.assertTrue('mailing_package' in labels)
        self.assertTrue('person' in labels)
        self.assertFalse('cat' in labels)
        self.assertFalse('cat_mouth' in labels)
        self.assertFalse('cat_eye' in labels)
        self.assertFalse('cat_nose' in labels)

    # Provided a video with no objects of interest, the Video class should not detect any objects
    def test_detect_no_objects(self, client):
        camera = Video(cameraSource="test_videos/no_objects.mp4", timeout=0)
        response = camera.get_frame()
        labels = response['labels']
        print(labels)
        self.assertEqual(len(labels), 0)
        self.assertFalse('mailing_package' in labels)
        self.assertFalse('person' in labels)
        self.assertFalse('cat' in labels)
        self.assertFalse('cat_mouth' in labels)
        self.assertFalse('cat_eye' in labels)
        self.assertFalse('cat_nose' in labels)


if __name__ =="__main__":
    unittest.main()