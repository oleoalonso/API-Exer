from flask import Flask, render_template, request
import pandas as pd
import csv

app = Flask(__name__)

# Requisição do webSite html para emissão de arquivo .CSV
# Necessario acessar API via webBrowser, selecionar arquivo .CSV e enviar
@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

# Retorno webSite html para exibição arquivo .CSV
@app.route("/data", methods=["GET", "POST"])
def data():
    if request.method == "POST":
        f = request.form["csvfile"]
        data = []
        with open(f) as file:
            csvfile = csv.reader(file)
            for row in csvfile:
                data.append(row)
        data = pd.DataFrame(data)        
        return render_template("data.html", data=data.to_html(header=False, index=False))

# Cadastramento informações arquivo .CSV
# OBS.: Necessário utilizar software como o POSTMAN PARA ADICIONAR O JSON, EXEMPLO:
# {
#     "FILME": "007 SEM TEMPO PARA MORRER",
#     "GENERO": "Acao",
#     "STATUS": "Locado"
# }
@app.route("/cadastrar/", methods=["POST"])
def incluir():
    user_info = request.json
    print(request.json)
    with open("acervoFilme.csv", "a", newline="") as cad:
        escrever = csv.writer(cad, delimiter=",")
        usuario = [user_info["FILME"], user_info["GENERO"], user_info["STATUS"]]   
        escrever. writerow(usuario)
    return "Cadastro de informações realizadas com sucesso!"

# Opção de deletar informações no arquivo .CSV
# Necessário utilizar software POSTMAN e executar através da url http://127.0.0.1:5000/deletar/<inserirLinha>
@app.route("/deletar/<id>", methods=["DELETE"])
def deletar(id):
    # Abre o arquivo para leitura
    with open("acervoFilme.csv", "r", encoding="utf-8") as cad:
        # Leitura do arquivo .CSV
        leitura = csv.reader(cad, delimiter=",")

        # Armazena o conteúdo do .CSV na variável
        data = list(leitura)
        print(data)

    #  Abre o arquivo para escrita
    with open("acervoFilme.csv", "w", encoding="utf-8") as cad:
        # Criando um objeto de escrita
        escrita = csv.writer(cad, delimiter=",")

        for linha in data:
            print(linha)
            codigo, nome, documento = linha

            if id != codigo:
                escrita.writerow(linha)

    return "Filme deletado com sucesso!"

# Execução da API
if __name__ == "__main__":
    app.run(debug=True)    