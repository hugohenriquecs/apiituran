from flask import Flask, jsonify, send_file
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
import xmltodict
import os 

app = Flask(__name__)

# URL base da API da Ituran
ITURAN_API_URL = "https://iweb.ituran.com.br/ituranwebservice3/Service3.asmx/GetAllPlatformsData?UserName=api@armac&Password=Api@2024Ituran@&ShowAreas=True&ShowStatuses=True&ShowMileageInMeters=False&ShowDriver=True"

# Credenciais de autenticação
ITURAN_USERNAME = "api@armac"
ITURAN_PASSWORD = "Api@2024Ituran@"

@app.route('/buscar_dados_plataforma', methods=['GET'])
def buscar_dados_plataforma():
    try:
        print(f"Requisição para URL: {ITURAN_API_URL}")

        # Fazendo a requisição GET para a API da Ituran com autenticação básica
        response = requests.get(ITURAN_API_URL, auth=HTTPBasicAuth(ITURAN_USERNAME, ITURAN_PASSWORD))
        print("Resposta recebida.")

        # Verifica se a resposta foi bem-sucedida
        if response.status_code == 200:
            # Carrega a resposta XML em um dicionário
            dados = xmltodict.parse(response.content)
            print("Dados recebidos:", dados)

            # Verifica se os dados estão na estrutura esperada
            if 'GetAllPlatformsData' in dados and 'GetAllPlatforms' in dados['GetAllPlatformsData']:
                lista_dados = dados['GetAllPlatformsData']['GetAllPlatforms']
                
                #Verifica se lista_dados é uma lista; se não, converte para uma lista de um único elemento
                if not isinstance(lista_dados, list):
                    lista_dados = [lista_dados]

                # Converte para DataFrame
                df = pd.DataFrame(lista_dados)
                print("DataFrame criado com sucesso.")

                # Salva o DataFrame em um arquivo Excel
                excel_file = 'dados_plataforma.xlsx'
                df.to_excel(excel_file, index=False)
                print('Excel salvo com sucesso.')

                # Envia o arquivo Excel para download
                return send_file(excel_file, as_attachment=True)
            else:
                return jsonify({"erro": "Estrutura de dados inesperada", "dados_recebidos": dados}), 500

        else:
            return jsonify({"erro": "Falha ao obter dados da API Ituran", "status_code": response.status_code}), response.status_code

    except Exception as e:
        print("Erro", e)
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
