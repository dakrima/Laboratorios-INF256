
import socket
from datetime import datetime

servidor_UDP = ("", 9001)
cliente_HTTP = ("localhost", 8000)
palabra_finalizar = "FINAL"

def finalizar(text: str) -> bool:
    msg_partes = text.strip().rsplit("-", 1)
    if len(msg_partes) == 2 and msg_partes[1].strip().upper() == palabra_finalizar:
        return True
    return len(text.rsplit("-", 3)) < 4

def anadir_mensaje(text: str) -> str:
    _timestamp, min_largo, _largo_actual, msg = text.rsplit("-", 3)
    extra = input("Palabra para agregar: ").strip()
    nuevo_msg = f"{msg} {extra}".strip()
    largo_actual = len(nuevo_msg.split())
    timestamp = datetime.now().isoformat(timespec="seconds")
    return f"{timestamp}-{min_largo}-{largo_actual}-{nuevo_msg}"

# HTTP a Servicio 4

def mandar_a_servicio_4(body_text: str):
    body_bytes = body_text.encode("utf-8")
    req = (
        f"POST /frase HTTP/1.1\r\n"
        f"Host: {cliente_HTTP[0]}:{cliente_HTTP[1]}\r\n"
        "Content-Type: text/plain; charset=utf-8\r\n"
        f"Content-Length: {len(body_bytes)}\r\n"
        "Connection: close\r\n\r\n"
    ).encode("utf-8") + body_bytes

    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.connect(cliente_HTTP)
    print("Mandando al servicio 4.")
    c.sendall(req)
    resp = b"" 
    while True:

        chunk = c.recv(4096)
        if not chunk:
            break
        resp += chunk
    c.close()

    try:
        _, body_raw = resp.split(b"\r\n\r\n", 1)
        return body_raw.decode("utf-8").strip()
    except ValueError:
        return ""


if __name__ == "__main__":

    # Servicio 2 a UDP

    u = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    u.bind(servidor_UDP)

    flag = False
    while not flag:
        data, addr = u.recvfrom(65535)
        text = data.decode("utf-8").strip()
        if not text:
            continue
        if finalizar(text):
            s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s2.connect(("localhost", 9000))
            s2.sendall(text.encode("utf-8"))
            s2.close()
            #flag = True
            print("FINALIZACIÓN obtenida. Close todo!")
            break
        else:
            http_body = anadir_mensaje(text)
            resp_body = mandar_a_servicio_4(http_body)
            

            if finalizar(resp_body):
                s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s2.connect(("localhost", 9000))
                s2.sendall(resp_body.encode("utf-8"))
                s2.close()
                #flag = True
                print("FINALIZACIÓN recibida de S4 y enviada a servicio 2 (TCP).")
                break


    u.close()
