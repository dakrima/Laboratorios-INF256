
from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime
import socket

servidor_HTTP = ("", 8000)
cliente_TCP = ("localhost", 9002)
palabra_finalizar = "FINAL"
archivo_txt = "mensaje_final.txt"

# TCP a Servicio 1

def mandar_a_servicio_1(text: str):
    print("Mandar a Servicio 1")
    data = (text.rstrip() + "\n").encode("utf-8")
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.connect(cliente_TCP)
    c.sendall(data)
    c.close()

def finalizar(text: str) -> bool:
    msg_partes = text.strip().rsplit("-", 1)
    if len(msg_partes) == 2 and msg_partes[1].strip().upper() == palabra_finalizar:
        return True
    return len(text.rsplit("-", 3)) < 4


class HandlerHTTP(BaseHTTPRequestHandler):
    def do_POST(self):
        n = int(self.headers.get("Content-Length", "0") or 0)
        body = self.rfile.read(n).decode("utf-8").strip()
        if not body:
            self.send_response(400); self.end_headers(); return

        if finalizar(body):
            self.send_response(200); self.end_headers()
            self.server.shutdown()
            return

        timestamp, min_largo, largo_actual, msg = body.rsplit("-", 3)
        min_largo = int(min_largo); largo_actual = int(largo_actual)

        if largo_actual >= min_largo:
            with open(archivo_txt, "a", encoding="utf-8") as f:
                f.write(f"{timestamp}-{msg}\n")

            final_body = f"{datetime.now().isoformat(timespec='seconds')}-{palabra_finalizar}"
            final_bytes = final_body.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(final_bytes)))
            self.send_header("Connection", "close")
            self.end_headers()
            self.wfile.write(final_bytes)
            self.server.shutdown()
            return
        else:
            extra = input("Palabra para agregar: ").strip()
            nuevo_msg = f"{msg} {extra}".strip()
            largo_actual = len(nuevo_msg.split())
            tcp_msg = f"{datetime.now().isoformat(timespec='seconds')}-{min_largo}-{largo_actual}-{nuevo_msg}"
            mandar_a_servicio_1(tcp_msg)


            resp_bytes = tcp_msg.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(resp_bytes)))
            self.end_headers()
            self.wfile.write(resp_bytes)

    def log_message(self, *args):
        pass

if __name__ == "__main__":
    HTTPServer(servidor_HTTP, HandlerHTTP).serve_forever()