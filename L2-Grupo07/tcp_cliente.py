
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
    udp_port = 9001
    http_port = 1080
    joke_txt = respuesta
    # print(f"LLEGA: {respuesta}")

    m_udp = re.search(r"UDP[_ ]?PORT[:=]\s*(\d+)", respuesta, re.IGNORECASE)
    m_http = re.search(r"HTTP[_ ]?PORT[:=]\s*(\d+)", respuesta, re.IGNORECASE)
    if m_udp:
        udp_port = int(m_udp.group(1))
    if m_http:
        http_port = int(m_http.group(1))

    m_joke = re.search(r"JOKE\s*[:=]\s*(.*)", respuesta, re.IGNORECASE)
    # print("Respuesta Guardada")
    print(m_joke)
    if m_joke:
        joke_txt = m_joke.group(1).strip()

    return udp_port, http_port, respuesta

def fase_tcp():
    print("== Fase TCP ==")
    print("Escribe comandos (GET, JOKE, EXIT). Escribe EXIT para terminar.\n")

    udp_port = None
    http_port = None
    joke_text = None

    while True:
        comando = input("> Ingresa un comando: ").strip().upper()
        if not comando:
            continue

        resp = enviar_comando_tcp(comando)
        print("< Respuesta:\n" + (resp or "(vacía)"))
        cond = 0
        u, h, j = extraer_puertos_y_joke(resp)
        if udp_port is None and u is not None:
            # print(f"CAMBIANDO2: {u}")
            udp_port = u
            cond += 1
        if http_port is None and h is not None:
            # print(f"CAMBIANDO1: {h}")
            http_port = h
            cond += 1
        if joke_text is None and j:
            # print(f"CAMBIANDO: {j}")
            joke_text = j
            cond += 1

        if comando == "EXIT" or cond == 3:
            cond = 0
            break

    return udp_port, http_port, joke_text

