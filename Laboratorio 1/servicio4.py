
from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime
import socket

servidor_HTTP = ("", 8000)
cliente_TCP = ("localhost", 9002)

def mandar_a_servicio_1(text: str):
    encoded = (text + "\n").encode()
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.connect(cliente_TCP)
    c.sendall(encoded)
    c.close()

class HandlerHTTP(BaseHTTPRequestHandler):
    def do_POST(self):
        n = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(n).decode().strip()

        _timestamp, min_largo, largo_actual, msg = body.split("-", 3)
        min_largo = int(min_largo); largo_actual = int(largo_actual)

        if largo_actual >= min_largo :
            final = f"{body} FINAL"
            mandar_a_servicio_1(final)
            self.send_response(200); self.end_headers()
        else : 
            extra = input("Palabra para agregar: ").strip()
            nuevo_msg = f"{msg} {extra}".strip()
            largo_actual = len(nuevo_msg.split())
            tcp_msg = f"{datetime.now().isoformat(timespec='seconds')}-{min_largo}-{largo_actual}-{nuevo_msg}"
            mandar_a_servicio_1(tcp_msg)
            self.send_response(200); self.end_headers()

    def log_message(self, *args):
        pass

if __name__ == "__main__":
    HTTPServer(servidor_HTTP, HandlerHTTP).serve_forever()