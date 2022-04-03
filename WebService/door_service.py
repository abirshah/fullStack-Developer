
class Door:
    def __init__(self):
        self.motion_log = []


    def open_door(self):
        print("opening door")
        try:
            urllib.request.urlopen('http://172.30.145.44:5000/open.html')
        except Exception as e:
            print("Error opening URL to send door activation signal")
