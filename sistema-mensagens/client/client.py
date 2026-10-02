import os
import time
import requests


SERVER_URL = os.getenv("SERVER_URL", "http://localhost:5000")
CLIENT_NAME = os.getenv("CLIENT_NAME", "alice")


def esperar_servidor():
    print(f"[{CLIENT_NAME.upper()}] Aguardando servidor...")

    while True:
        try:
            resposta = requests.get(f"{SERVER_URL}/usuarios")

            if resposta.status_code == 200:
                print(f"[{CLIENT_NAME.upper()}] Servidor disponível!")
                break

        except requests.exceptions.RequestException:
            pass

        time.sleep(1)


def registrar_usuario():
    resposta = requests.post(
        f"{SERVER_URL}/usuarios",
        json={"nome": CLIENT_NAME}
    )

    print(
        f"[{CLIENT_NAME.upper()}] "
        f"Registro: HTTP {resposta.status_code}"
    )

    return resposta


def enviar_mensagem(destinatario, conteudo):
    resposta = requests.post(
        f"{SERVER_URL}/mensagens",
        json={
            "remetente": CLIENT_NAME,
            "destinatario": destinatario,
            "conteudo": conteudo
        }
    )

    print(
        f"[{CLIENT_NAME.upper()}] "
        f"Envio para {destinatario}: "
        f"HTTP {resposta.status_code}"
    )

    if resposta.ok:
        print(f"[{CLIENT_NAME.upper()}] Mensagem enviada com sucesso!")


def consultar_mensagens_nao_lidas():
    resposta = requests.get(
        f"{SERVER_URL}/mensagens",
        params={
            "destinatario": CLIENT_NAME,
            "lida": "false"
        }
    )

    print(
        f"[{CLIENT_NAME.upper()}] "
        f"Consulta de mensagens não lidas: "
        f"HTTP {resposta.status_code}"
    )

    if resposta.ok:
        mensagens = resposta.json()

        for mensagem in mensagens:
            print(
                f"[{CLIENT_NAME.upper()}] "
                f"Mensagem de {mensagem['remetente']}: "
                f"{mensagem['conteudo']}"
            )

        return mensagens

    return []


def marcar_como_lida(id_mensagem):
    resposta = requests.patch(
        f"{SERVER_URL}/mensagens/{id_mensagem}",
        json={"lida": True}
    )

    print(
        f"[{CLIENT_NAME.upper()}] "
        f"PATCH mensagem {id_mensagem}: "
        f"HTTP {resposta.status_code}"
    )


def main():
    print(f"\n[{CLIENT_NAME.upper()}] Iniciando cliente...")

    esperar_servidor()
    registrar_usuario()

    # Pequena espera para permitir que os outros clientes
    # também sejam registrados.
    time.sleep(3)

    if CLIENT_NAME == "alice":
        enviar_mensagem(
            "bob",
            "Oi Bob! Aqui é a Alice."
        )

    elif CLIENT_NAME == "carol":
        enviar_mensagem(
            "bob",
            "Oi Bob! Aqui é a Carol."
        )

    elif CLIENT_NAME == "bob":
        # Espera Alice e Carol enviarem as mensagens.
        time.sleep(3)

        mensagens = consultar_mensagens_nao_lidas()

        if mensagens:
            id_mensagem = mensagens[0]["id"]

            print(
                f"[BOB] Marcando mensagem "
                f"{id_mensagem} como lida..."
            )

            marcar_como_lida(id_mensagem)

            time.sleep(1)

            print("[BOB] Consultando novamente...")

            consultar_mensagens_nao_lidas()


if __name__ == "__main__":
    main()