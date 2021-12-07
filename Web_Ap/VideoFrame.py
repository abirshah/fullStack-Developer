class Frame:
    _imageNumber = 0
    filename = "image"
    content = "blank"

    def __init__(self):
        Frame._imageNumber += 1
        self.filename = self.filename + str(Frame._imageNumber)

    def save_frame(self):
        print("saving " + self.filename)

    def format_db2python(self):
        self.content = self.content #CODE

    def format_python2db(self):
        self.content = self.content #CODE


tst = Frame()
tst.save_frame()

