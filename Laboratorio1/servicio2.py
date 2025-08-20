
import socket
from datetime import datetime

cliente_UPD = ("localhost", 9001) 
servidor_TCP = ("", 9000)
palabra_finalizar = "FINAL"

def finalizar(text: str) -> bool:
    msg_partes = text.strip().rsplit("-", 1)
    if len(msg_partes) == 2 and msg_partes[1].strip().upper() == palabra_finalizar:
        return True
    return len(text.rsplit("-", 3)) < 4

# UDP a Servicio 3

def mandar_a_servicio_3(text: str):
    u = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    u.sendto(text.encode("utf-8"), cliente_UPD)
    u.close()

def anadir_mensaje(text: str) -> str:
    _timestamp, min_largo, _largo_actual, msg = text.rsplit("-", 3)
    extra = input("Palabra para agregar: ").strip()
    nuevo_msg = f"{msg} {extra}".strip()
    largo_actual = len(nuevo_msg.split())
    timestamp = datetime.now().isoformat(timespec="seconds")
    return f"{timestamp}-{min_largo}-{largo_actual}-{nuevo_msg}"


if __name__ == "__main__":


    # Servicio 1 a TCP

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
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect(("localhost", 9002))
                sock.sendall(text.encode("utf-8"))
                sock.close()
                flag = True
                print("FINALIZACIÓN mandado al servicio 1.")
            else:
                udp_msg = anadir_mensaje(text)
                mandar_a_servicio_3(udp_msg)
                print("Mandando al servicio 3.")

    s.close()
