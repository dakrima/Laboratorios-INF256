import socket
import os
import json
from config import HOST, SOCKET_TIMEOUT

def construir_post(frase, grupo_id, puerto_http):
    body = json.dumps({"frase": frase, "grupo": grupo_id}, ensure_ascii=False).encode("utf-8")
    req = (
        "POST /frase/ HTTP/1.1\r\n"
        "Host: " + HOST + ":" + str(puerto_http) + "\r\n"
        "Content-Type: application/json; charset=utf-8\r\n"
        "Content-Length: " + str(len(body)) + "\r\n"
        "Connection: close\r\n\r\n"
    ).encode("utf-8") + body
    return req

def post_frase(frase, grupo_id, puerto_http):
    req = construir_post(frase, grupo_id, puerto_http)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(SOCKET_TIMEOUT)
    s.connect((HOST, puerto_http))
    s.sendall(req)
    partes = []
    try:
        while True:
            data = s.recv(4096)
            if not data:
                break
            partes.append(data)
    except socket.timeout:
        pass
    s.close()

    raw = b"".join(partes).decode("utf-8", "ignore")
    primera = raw.splitlines()[0] if raw else ""
    try:
        status = int(primera.split()[1])
    except Exception:
        status = -1
    cuerpo = raw.split("\r\n\r\n", 1)[1] if "\r\n\r\n" in raw else ""
    return status, cuerpo.strip()
