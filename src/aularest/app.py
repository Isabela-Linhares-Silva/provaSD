"""Exemplo funcional de API REST."""

from flask import Flask, jsonify, request

app = Flask(__name__)
app.json.ensure_ascii = False  # pyright: ignore[reportAttributeAccessIssue]

itens = {1: {"id": 1, "nome": "Teclado", "preco": 120.0}}


@app.route("/itens/<int:id_item>", methods=["GET", "PUT", "PATCH", "DELETE", "HEAD"])
def item(id_item: int):
    """Rota que usa id como entrada.

    Nesta rota iremos tratar todos os métodos HTTP, exceto o POST e o GET sem id
    fornecido.
    """
    # Nós precisamos conferir se o item já existe aqui no recurso
    # e responder adequadamente, em "HTTP"ês
    if id_item not in itens:
        return jsonify({"erro": "Item não encontrado"}), 404

    if request.method == "GET":
        print("Recebi um GET")

        return jsonify(itens[id_item]), 200

    elif request.method == "PUT":
        print("Recebi um PUT")

        dados = request.get_json()

        itens[id_item] = {"id": id_item, "nome": dados["nome"], "preco": dados["preco"]}

        return jsonify(itens[id_item]), 200

    elif request.method == "PATCH":
        print("Recebi um PATCH")

        dados = request.get_json()

        if "nome" in dados:
            itens[id_item]["nome"] = dados["nome"]

        if "preco" in dados:
            itens[id_item]["preco"] = dados["preco"]

        return jsonify(itens[id_item]), 200

    elif request.method == "DELETE":
        print("Recebi um DELETE")

        del itens[id_item]

        return "", 204  # por que acham que aqui a gente usa o 204?

    elif request.method == "HEAD":  # nesse último, precisamos mesmo de elif?
        print("Recebi um HEAD")

        return "", 200

    return jsonify("{'error': 'Instrução desconhecida'}"), 200  # 200 mesmo?


@app.get("/itens")
def todos_os_itens():
    """E se quisermos entregar uma lista de todos os itens?"""

    return jsonify(itens), 200  # Se esta lista crescer muito
    # talvez fosse legal a gente fazer paginação
    # retornando algo como (inventei números no exemplo):
    # {
    #  "pagina": 1,
    #  "por_pagina": 2,
    #  "total_itens": 5,
    #  "total_paginas": 3,
    #  "itens": [
    #    {
    #      "id": 1,
    #      "nome": "Teclado",
    #      "preco": 120.0
    #    },
    #    {
    #      "id": 2,
    #      "nome": "Capacete",
    #      "preco": 110.0
    #    }
    #  ]
    # }
    #
    # a gente conseguiria enviar esses dados para o recurso com
    # query parameters (quando uma url fica: http://google.com/search?q=gato o "q"
    # ali é um query parameter e pode ser acessado no objeto request do flask como
    # busca = request.args.get("q"))


@app.post("/itens")
def criar_item():
    """Rota para inserir itens no nosso recurso."""
    print("Recebi um POST")

    dados = request.get_json()

    novo_id = max(itens.keys(), default=0) + 1  # Por que max e não len?

    novo_item = {"id": novo_id, "nome": dados["nome"], "preco": dados["preco"]}

    itens[novo_id] = novo_item

    return jsonify(novo_item), 201


def main():
    app.run("0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
