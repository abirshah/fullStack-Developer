import datetime

from .shared import db, ma


class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    classes = db.Column(db.String(100))
    ts = db.Column(db.TIMESTAMP, nullable=False, default=datetime.datetime.now())
    video = db.Column(db.String(100))
    access_granted = db.Column(db.BOOLEAN)

    def __init__(self, classes, video, access_granted):
        self.classes = classes
        self.video = video
        self.access_granted = access_granted


class EventsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'classes', 'ts', 'video', 'access_granted')
