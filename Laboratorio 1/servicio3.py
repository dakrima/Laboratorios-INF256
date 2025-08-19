
import socket
from datetime import datetime

servidor_UDP = ("", 9001)
cliente_HTTP = ("localhost", 8000)

# Servicio 2 a UDP 

u = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
u.bind(servidor_UDP)
data, addr = u.recvfrom(65535)
u.close()
text = data.decode().strip()

# Preparar el nuevo mensaje

_timestamp, min_largo, largo_actual, msg = text.split("-", 3)
extra = input("Palabra para agregar: ").strip()
nuevo_msg = f"{msg} {extra}".strip()
largo_actual = len(nuevo_msg.split())
http_body = f"{datetime.now().isoformat(timespec='seconds')}-{min_largo}-{largo_actual}-{nuevo_msg}"

# HTTP a Servicio 4

body_bytes = http_body.encode()
headers = (
    f"POST /frase HTTP/1.1\r\n"
    f"Host: {cliente_HTTP[0]}:{cliente_HTTP[1]}\r\n"
    "Content-Type: text/plain; charset=utf-8\r\n"
    f"Content-Length: {len(body_bytes)}\r\n"
    "Connection: close\r\n\r\n"
).encode()

http_request = headers + body_bytes
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect(cliente_HTTP)
c.sendall(http_request)
c.close()

