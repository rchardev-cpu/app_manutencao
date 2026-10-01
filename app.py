from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
import csv
import os
from datetime import datetime


app = Flask(__name__)


# Localização do arquivo CSV
PASTA_PROJETO = os.path.dirname(os.path.abspath(__file__))
ARQUIVO = os.path.join(PASTA_PROJETO, "solicitacoes.csv")


# Campos utilizados no CSV
CAMPOS = [
    "id",
    "nome",
    "tipo_usuario",
    "sala",
    "equipamento",
    "descricao",
    "data",
    "status"
]


# Carrega as solicitações existentes no CSV
def carregar_solicitacoes():
    solicitacoes = []

    if os.path.exists(ARQUIVO):
        with open(
            ARQUIVO,
            "r",
            newline="",
            encoding="utf-8"
        ) as arquivo:
            leitor = csv.DictReader(arquivo)
            solicitacoes.extend(leitor)

    return solicitacoes


# Salva as solicitações no CSV
def salvar_solicitacoes(solicitacoes):
    with open(
        ARQUIVO,
        "w",
        newline="",
        encoding="utf-8"
    ) as arquivo:
        escritor = csv.DictWriter(
            arquivo,
            fieldnames=CAMPOS
        )

        escritor.writeheader()
        escritor.writerows(solicitacoes)


# Gera automaticamente o próximo ID
def gerar_novo_id(solicitacoes):
    ids = []

    for solicitacao in solicitacoes:
        try:
            ids.append(int(solicitacao["id"]))
        except (ValueError, KeyError):
            pass

    return str(max(ids, default=0) + 1)


# Página inicial
@app.route("/")
def inicio():
    solicitacoes = carregar_solicitacoes()

    return render_template(
        "index.html",
        solicitacoes=solicitacoes
    )


# Cadastro de uma nova solicitação
@app.route("/cadastrar", methods=["POST"])
def cadastrar():
    solicitacoes = carregar_solicitacoes()

    nova_solicitacao = {
        "id": gerar_novo_id(solicitacoes),
        "nome": request.form.get("nome", "").strip(),
        "tipo_usuario": request.form.get("tipo_usuario", "").strip(),
        "sala": request.form.get("sala", "").strip(),
        "equipamento": request.form.get("equipamento", "").strip(),
        "descricao": request.form.get("descricao", "").strip(),
        "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "status": "Pendente"
    }

    # Campos obrigatórios
    campos_obrigatorios = [
        "nome",
        "tipo_usuario",
        "sala",
        "equipamento",
        "descricao"
    ]

    # Verifica se todos os campos foram preenchidos
    if all(
        nova_solicitacao[campo]
        for campo in campos_obrigatorios
    ):
        solicitacoes.append(nova_solicitacao)
        salvar_solicitacoes(solicitacoes)

    return redirect("/")


# Concluir uma solicitação
@app.route("/concluir/<id_solicitacao>")
def concluir(id_solicitacao):
    solicitacoes = carregar_solicitacoes()

    for solicitacao in solicitacoes:
        if solicitacao.get("id") == id_solicitacao:
            solicitacao["status"] = "Concluído"
            break

    salvar_solicitacoes(solicitacoes)

    return redirect("/")


# Inicia o servidor
if __name__ == "__main__":
    app.run(debug=True)

