from array import array
from http.server import BaseHTTPRequestHandler, HTTPServer
from multiprocessing.dummy import Array
import ast

array = []
class Server(BaseHTTPRequestHandler):

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself

        if self.path == '/recv':
            print(post_data)
            print(str(post_data)[2:-1])
            array.append(str(post_data)[2:-1])
            print(array)

        print(array)
        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

    def do_GET(self):
        if str(self.path)[:5] == '/recv':
            if len(array) != 0:
                y = 0
                found = False
                index = 0
                for x in array:
                    x = ast.literal_eval(x)
                    if str(x["from"]) == self.path[6:] and found == False:
                        found = True
                        y = x
                    if found == False:
                        index += 1
                if found == False:
                    self._set_response()
                    self.wfile.write("ARRAY EMPTY".encode('utf-8'))   
                else:
                    self._set_response()
                    self.wfile.write(str(y).encode('utf-8'))
                    print(index)
                    array.pop(index)
            else: 
                self._set_response()
                self.wfile.write("ARRAY EMPTY".encode('utf-8'))

def run(server_class=HTTPServer, handler_class=Server, port=8080):
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