#!/usr/bin/env python
import SimpleHTTPServer
import SocketServer
import json
import socket


class MyRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/pi_remote/discover":
          self._success_response()
          response = {"hostname":socket.gethostname()}
          json.dump(JsonResponseFormatter.success_with_data(response), self.wfile) 
        else:
          self._failure_response()
          json.dump(JsonResponseFormatter.failure_with_data({}), self.wfile) 
    
    def _success_response(self):  
        self.send_response(200)
        self.send_header("Content-type:", "application/json")
        self.wfile.write("\n")
    
    def _failure_response(self):  
        self.send_response(404)
        self.send_header("Content-type:", "application/json")
        self.wfile.write("\n")

class JsonResponseFormatter:
  @classmethod
  def success_with_data(cls, data):
    return {"status":"success", "data":data}

  @classmethod
  def failure_with_data(cls, data):
    return {"status":"fail", "data":data}
      
Handler = MyRequestHandler
server = SocketServer.TCPServer(('0.0.0.0', 8080), Handler)

server.serve_forever()
