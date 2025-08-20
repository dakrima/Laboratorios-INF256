
import socket
from datetime import datetime

cliente_TCP = ("localhost", 9000)
servidor_TCP = ("", 9002)
palabra_finalizar = "FINAL"

def finalizar(text: str) -> bool:
    msg_partes = text.strip().rsplit("-", 1)
    if len(msg_partes) == 2 and msg_partes[1].strip().upper() == palabra_finalizar:
        return True
    return len(text.rsplit("-", 3)) < 4

## TCP a Servicio 2

def mandar_a_servicio_2(text: str):
    data = (text.rstrip() + "\n").encode("utf-8")
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.connect(cliente_TCP)
    c.sendall(data)
    c.close()

def crear_mensaje(min_largo: int, first: str) -> str:
    timestamp = datetime.now().isoformat(timespec="seconds")
    return f"{timestamp}-{min_largo}-1-{first.strip()}"


if __name__ == "__main__" :

    min_largo = int(input("Largo mínimo: ").strip())
    first = input("Palabra inicial: ").strip()
    msg = f"{datetime.now().isoformat(timespec='seconds')}-{min_largo}-{len(first.split())}-{first}"
    mandar_a_servicio_2(msg)
    print(f"Mensaje enviado al servicio 2!!!: {msg}")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(servidor_TCP)
    s.listen(1)

    flag = False
    while not flag:
        conn, addr = s.accept()
        with conn:
            text = conn.recv(65535).decode("utf-8").strip()
            if not text:
                continue
            if finalizar(text):
                print("Recibido FINAL. Close!")
                flag = True
                continue

            _timestamp, min_str, _largo_actual, msg = text.rsplit("-", 3)
            extra = input("S1 - Palabra para agregar: ").strip()
            nuevo_msg = f"{msg} {extra}".strip()
            nuevo_largo = len(nuevo_msg.split())

            tcp_msg = f"{datetime.now().isoformat(timespec='seconds')}-{min_str}-{nuevo_largo}-{nuevo_msg}"
            mandar_a_servicio_2(tcp_msg)
            print("Mandando al servicio 2.")

    s.close()

