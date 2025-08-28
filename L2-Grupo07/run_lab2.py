
import os
from config import GRUPO_ID, UDP_PORT as UDP_DEFAULT, HTTP_PORT as HTTP_DEFAULT
from tcp_cliente import fase_tcp
from udp_cliente import enviar_udp_y_recibir
from http_cliente import post_frase

def main():
    udp_port, http_port, joke_text = fase_tcp()
    if udp_port is None:
        udp_port = UDP_DEFAULT
    if http_port is None:
        http_port = HTTP_DEFAULT

    print("\n== Resumen TCP ==")
    print("UDP_PORT:", udp_port)
    print("HTTP_PORT:", http_port)
    print("JOKE:", joke_text)

    if udp_port is None or not joke_text:
        print("Falta UDP_PORT o no se obtuvo JOKE. Ajusta el parsing o config.")
        return
    print("\n== Fase UDP ==")
    frase = enviar_udp_y_recibir(joke_text, udp_port)
    if not frase:
        print("No se recibió frase por UDP.")
        return
    print("Frase UDP:", frase)

    if http_port is None:
        print("Falta HTTP_PORT. Ajusta el parsing o config.")
        return
    print("\n== Fase HTTP ==")
    status, body = post_frase(frase, GRUPO_ID, http_port)
    print("HTTP status:", status)
    print("Cuerpo respuesta:")
    print(body if body else "(sin cuerpo)")

if __name__ == "__main__":
    main()
