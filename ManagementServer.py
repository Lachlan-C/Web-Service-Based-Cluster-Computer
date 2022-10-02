from hashlib import new
import grequests
from array import array
from http.server import BaseHTTPRequestHandler, HTTPServer
from multiprocessing.dummy import Array
import ast
from os.path import exists
from MPI import get_IP, get_num_nodes
import subprocess
import requests

def CheckServersAndUpdate():
    ServerList = open('servers.txt', 'r')
    lines = ServerList.readlines()
    newlist = []
    for i in lines:
        url = 'http://' + str(i) + ':8081/ping'
        message = requests.get(url).text
        if message == "Server Online":
            newlist += i
    print(newlist)

array = []
class Server(BaseHTTPRequestHandler):

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself

        if self.path[:8] == '/upload/':
            file = str(self.path[8:])
            print(file)
            print(post_data)
            
            f = open(file,"wb")
            f.write(post_data)
            f.close()

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

    def do_GET(self):
        if str(self.path)[:5] == '/ping':
            self._set_response()
            self.wfile.write("Server Online".encode('utf-8'))
        if str(self.path)[:5] == '/run/':
            file_exists = exists(str(self.path[5:]) + ".py")
            if file_exists:
                print("Running code ", str(self.path[5:]) + ".py")
                print(subprocess.Popen(["python3", str(self.path[5:]) + ".py"]))
                response = "File ran " + str(self.path[5:] + ".py")
                self._set_response()
                self.wfile.write(response.encode('utf-8'))
            else:
                self._set_response()
                self.wfile.write("File not found".encode('utf-8'))

        # Not Working Need to fix
        if str(self.path)[:8] == '/runall/':
            file = str(self.path[8:]) + ".py"
            
            node_urls = []
            for i in range(get_num_nodes()):
                url = 'http://' + str(get_IP(i)) + ':8081/run/' + str(self.path[8:])
                node_urls.append(url)
            print("Running on Nodes ", node_urls)

            rs = (grequests.get(u) for u in node_urls)
            responses = grequests.map(rs)
            text = list(map(lambda d : d.text if d else None, responses))
            print(text)

            self._set_response()
            self.wfile.write("test".encode('utf-8'))


def run(server_class=HTTPServer, handler_class=Server, port=8081):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print("Starting server")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()


# https://gist.github.com/mdonkers/63e115cc0c79b4f6b8b3a6b797e485c7 