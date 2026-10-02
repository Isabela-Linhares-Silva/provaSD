from flask import Flask, jsonify, request

app = Flask(__name__)

app.json.ensure_ascii = False

usuarios = {}
mensagens = {}

proximo_usuario_id = 1
proxima_mensagem_id = 1


@app.post("/usuarios")
def criar_usuario():
    global proximo_usuario_id

    dados = request.get_json()

    if not dados or "nome" not in dados:
        return jsonify({"erro": "Nome do usuário é obrigatório"}), 400

    nome = dados["nome"]

    if nome in usuarios:
        return jsonify({"erro": "Usuário já cadastrado"}), 409

    usuario = {
        "id": proximo_usuario_id,
        "nome": nome
    }

    usuarios[nome] = usuario
    proximo_usuario_id += 1

    print(f"[SERVIDOR] Usuário cadastrado: {nome}")

    return jsonify(usuario), 201


@app.get("/usuarios")
def listar_usuarios():
    return jsonify(list(usuarios.values())), 200


@app.post("/mensagens")
def criar_mensagem():
    global proxima_mensagem_id

    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "JSON obrigatório"}), 400

    campos_obrigatorios = ["remetente", "destinatario", "conteudo"]

    for campo in campos_obrigatorios:
        if campo not in dados:
            return jsonify({
                "erro": f"Campo '{campo}' é obrigatório"
            }), 400

    remetente = dados["remetente"]
    destinatario = dados["destinatario"]
    conteudo = dados["conteudo"]

    if remetente not in usuarios:
        return jsonify({"erro": "Remetente não cadastrado"}), 404

    if destinatario not in usuarios:
        return jsonify({"erro": "Destinatário não cadastrado"}), 404

    mensagem = {
        "id": proxima_mensagem_id,
        "remetente": remetente,
        "destinatario": destinatario,
        "conteudo": conteudo,
        "lida": False
    }

    mensagens[proxima_mensagem_id] = mensagem
    proxima_mensagem_id += 1

    print(
        f"[SERVIDOR] Mensagem enviada: "
        f"{remetente} -> {destinatario} "
        f"(id={mensagem['id']})"
    )

    return jsonify(mensagem), 201


@app.get("/mensagens")
def listar_mensagens():
    destinatario = request.args.get("destinatario")
    remetente = request.args.get("remetente")
    lida = request.args.get("lida")

    resultado = list(mensagens.values())

    if destinatario:
        resultado = [
            mensagem for mensagem in resultado
            if mensagem["destinatario"] == destinatario
        ]

    if remetente:
        resultado = [
            mensagem for mensagem in resultado
            if mensagem["remetente"] == remetente
        ]

    if lida is not None:
        valor_lida = lida.lower() == "true"

        resultado = [
            mensagem for mensagem in resultado
            if mensagem["lida"] == valor_lida
        ]

    return jsonify(resultado), 200


@app.patch("/mensagens/<int:id_mensagem>")
def atualizar_mensagem(id_mensagem):
    if id_mensagem not in mensagens:
        return jsonify({"erro": "Mensagem não encontrada"}), 404

    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "JSON obrigatório"}), 400

    if "lida" in dados:
        mensagens[id_mensagem]["lida"] = dados["lida"]

    print(
        f"[SERVIDOR] Mensagem {id_mensagem} "
        f"atualizada: lida={mensagens[id_mensagem]['lida']}"
    )

    return jsonify(mensagens[id_mensagem]), 200


def main():
    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()