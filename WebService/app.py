from flask import Flask, render_template, Response
from camera import Video
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os.path
from Services.s3_service import S3Service

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
#Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:abir1971@pet-project.cqlvbpbplnsv.us-east-2.rds.amazonaws.com/automated_pet_door'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

@app.route('/')
def index():
    return render_template('index.html')


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/video')
def video():
    return Response(gen(Video()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


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
    app.run(debug=True)
