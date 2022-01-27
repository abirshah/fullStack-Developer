"""
Source
https://www.youtube.com/watch?v=hFNZ6kdBgO0&ab_channel=howCode
login at http://192.168.0.43:3000/index.html
"""


from http.server import HTTPServer, BaseHTTPRequestHandler


#HOST = '192.168.0.43'  #RasberryPI wlan1
#HOST = '192.168.0.42'  #RasberryPI wlan0
#HOST = '169.254.12.42'  #Ethernet
PORT = 3000

class RP_Server(BaseHTTPRequestHandler):

    def do_GET(self):
        print("Get block: " + str(self) )
        if self.path == '/':
            self.path = '/index.html'
        try:
            file_to_open = open(self.path[1:]).read()
            self.send_response(200)
        except:
            file_to_open = "File not found"
            self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes(file_to_open, 'utf-8'))


print("Running server on RasberryPI")
server = HTTPServer((HOST, PORT), RP_Server)
server.serve_forever()
