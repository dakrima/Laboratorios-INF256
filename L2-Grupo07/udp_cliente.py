import socket
import os
from config import HOST, SOCKET_TIMEOUT, GRUPO_ID

def enviar_udp_y_recibir(texto, puerto_udp):
    u = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    u.settimeout(SOCKET_TIMEOUT)
    texto += GRUPO_ID
    u.sendto(texto.encode("utf-8"), (HOST, puerto_udp))
    try:
        data, _addr = u.recvfrom(4096)
        u.close()
        return data.decode("utf-8", "ignore").strip()
    except socket.timeout:
        u.close()
        return ""
