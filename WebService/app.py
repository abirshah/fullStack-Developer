# Core Library modules
from typing import Optional
from flask import Flask, render_template, Response, request, Blueprint, jsonify, redirect
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from camera import Video
from Models.shared import db, ma
from Models.events import Events, EventsSchema
import os.path
from Services.s3_service import S3Service
from Config import config
import urllib.request

db = SQLAlchemy()

motion_log = []

def open_door():
    print("opening door")
    urllib.request.urlopen('http://192.168.0.42:5000/open.html')
	

def create_app(cfg: Optional[config.Config] = None) -> Flask:
    if cfg is None:
        cfg = config.Config()
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(cfg)

    CORS(app)
    basedir = os.path.abspath(os.path.dirname(__file__))
    # Init db
    db.init_app(app)
    # Init ma
    ma.init_app(app)

    # Simple route the veryify the health of the web service
    @app.route('/health_check')
    def health_check():
        return Response(status=200)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/events', methods=['POST'])
    def add_event():
        classes = request.json['classes']
        video = request.json['video']
        access_granted = request.json['access_granted']

        new_event = Events(classes=str(classes), video=video, access_granted=access_granted)
        db.session.add(new_event)
        db.session.commit()
        return Response(status=200)

    @app.route('/events', methods=['GET'])
    def get_events():
        all_events = Events.query.all()
        events_schema = EventsSchema(many=True)
        result = events_schema.dump(all_events)
        return jsonify(result)

    @app.route('/video/url', methods=['POST'])
    def generate_video_url():
        video_key = request.json['video']
        s3_service = S3Service()
        response = s3_service.generate_url(bucket='video-snapshots', key=video_key)
        return jsonify({'videoUrl': response})
		
    @app.route('/motion/<timestamp>')
    def motion_detection(timestamp):
        motion_log.append(timestamp)
        print("motion detected at: " + timestamp)
        return render_template('index.html')
        #return (f" Motion Detected at: " + timestamp)

    def gen(camera):
        while True:
            response = camera.get_frame()
            frame = response["frame"]
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

    @app.route('/video')
    def video():
        return Response(gen(Video(cameraSource=app.config.get("CAMERA"))),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
						
    @app.route('/open.html')
    def goHome():
        return render_template('index.html')
		
		
    @app.route('/submitbutton', methods=['POST'])
    def submitbutton():
        open_door()
        return render_template('index.html')
	
    return app


if __name__ == "__main__":
    s3_service = S3Service()
    if not os.path.exists('weight_files/yolov4.weights'):
        print("Downloading weight file yolov4.weights")
        s3_service.download_file(key='yolov4.weights', bucket='weightfiles', filename='weight_files/yolov4.weights')

    if not os.path.exists('weight_files/yolov4-custom_10000.weights'):
        print("Downloading weight file yolov4-custom_10000.weights")
        s3_service.download_file(key='yolov4-custom_10000.weights', bucket='weightfiles',
                                 filename='weight_files/yolov4-custom_10000.weights')

    if not os.path.exists('weight_files/yolov4-custom_bird_mail_new.weights'):
        print("Downloading weight file yolov4-custom_bird_mail_new.weights")
        s3_service.download_file(key='yolov4-custom_bird_mail_new.weights', bucket='weightfiles',
                                 filename='weight_files/yolov4-custom_bird_mail_new.weights')
								 
    app = create_app()
    # app.run(host='127.0.0.1', port=8000)
    app.run(host='192.168.0.56', port=8000)
