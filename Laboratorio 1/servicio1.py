
import socket
from datetime import datetime

cliente_TCP = ("localhost", 9000)
servidor_TCP = ("", 9002)

min_largo = int(input("[S1] Largo mínimo: ").strip())
first = input("[S1] Palabra inicial: ").strip()
timestamp = datetime.now().isoformat(timespec="seconds")
msg = f"{timestamp}-{min_largo}-{1}-{first}"

## TCP a Servicio 2

print(f"Conectando a {cliente_TCP}")
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect(cliente_TCP)
c.sendall((msg + "\n").encode())
c.close()
print(f"Enviado: {msg}\n")

## Servicio 4 a TCP

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(servidor_TCP)
s.listen(1)
conn, addr = s.accept()
print(f"Conexión aceptada de {addr}")
data = conn.recv(9999)
text = data.decode().strip()
print("Mensaje:", text)
conn.close(); s.close()