
import socket
from datetime import datetime

cliente_UPD = ("localhost", 9001) 
servidor_TCP = ("", 9000)

# Servicio 1 a TCP

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(servidor_TCP); s.listen(1)
print(f"Escuchando en :{servidor_TCP[1]}")
conn, addr = s.accept()
print(f"Conexión aceptada de {addr}")
raw = conn.recv(9999)
line = raw.decode().strip()
print("Mensaje:", line)
conn.close(); s.close()

# Preparar el nuevo mensaje

_timestamp, min_largo, largo_actual, msg = line.split("-", 3)
extra = input("Palabra para agregar: ").strip()
nuevo_msg = f"{msg} {extra}".strip()
largo_actual = len(nuevo_msg.split())
udp_msg = f"{datetime.now().isoformat(timespec='seconds')}-{min_largo}-{largo_actual}-{nuevo_msg}"

# UDP a Servicio 3

u = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_bytes = udp_msg.encode()
u.sendto(udp_bytes, cliente_UPD)
u.close()
print(f"Enviado: {udp_msg}")

