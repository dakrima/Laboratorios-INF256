
import socket
import os
import re
from config import HOST, TCP_PORT, SOCKET_TIMEOUT

palabra_finalizar = "FINAL"

def finalizar(texto):
    partes = texto.strip().rsplit("-", 1)
    return len(partes) == 2 and partes[1].strip().upper() == palabra_finalizar

def enviar_comando_tcp(comando):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(SOCKET_TIMEOUT)
    s.connect((HOST, TCP_PORT))
    s.sendall((comando.strip() + "\n").encode("utf-8"))
    trozos = []
    try:
        while True:
            data = s.recv(4096)
            if not data:
                break
            trozos.append(data.decode("utf-8", "ignore"))
    except socket.timeout:
        pass
    s.close()
    return "".join(trozos).strip()

def extraer_puertos_y_joke(respuesta):
    udp_port = None
    http_port = None
    joke_txt = None

    m_udp = re.search(r"UDP[_ ]?PORT[:=]\s*(\d+)", respuesta, re.IGNORECASE)
    m_http = re.search(r"HTTP[_ ]?PORT[:=]\s*(\d+)", respuesta, re.IGNORECASE)
    if m_udp:
        udp_port = int(m_udp.group(1))
    if m_http:
        http_port = int(m_http.group(1))

    m_joke = re.search(r"JOKE\s*[:=]\s*(.*)", respuesta, re.IGNORECASE)
    if m_joke:
        joke_txt = m_joke.group(1).strip()

    return udp_port, http_port, joke_txt

def fase_tcp():
    print("== Fase TCP ==")
    udp_port = None
    http_port = None
    joke_text = None

    for comando in ("GET", "JOKE", "EXIT"):
        print("> Enviando:", comando)
        resp = enviar_comando_tcp(comando)
        print("< Respuesta:" + (resp or "(vacía)"))
        u, h, j = extraer_puertos_y_joke(resp)
        if udp_port is None and u is not None:
            udp_port = u
        if http_port is None and h is not None:
            http_port = h
        if joke_text is None and j:
            joke_text = j

    return udp_port, http_port, joke_text
