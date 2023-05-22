from flask import Flask, request
from flask_cors import CORS, cross_origin
import json
from collections import defaultdict

cartas_apostolicas = defaultdict(dict)
cartas = defaultdict(dict)
enciclicas = defaultdict(dict)
motus= defaultdict(dict)
pontifices = defaultdict(dict)
viagens = defaultdict(dict)
 #------------------------------------------------------------------------------
aux = open("cartas_apostolicas.json","r")
cartas_apostolicas = json.load(aux)

aux = open("cartas.json","r")
cartas = json.load(aux)

aux = open("enciclicas.json","r")
enciclicas = json.load(aux)

aux = open("motus_proprio.json","r")
motus = json.load(aux)

aux = open("pontifices.json","r")
pontifices = json.load(aux)

aux =open("viagens.json","r")
viagens = json.load(aux)
 #-----------------------------------------------------------------------------
app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def index():
    data = {"msg":"esta é uma aplicação para a discplina exa844"}
    data = json.dumps(data,indent=4, ensure_ascii=False)
    return data

@app.route('/teste', methods=['GET'])
def teste():
    aux =open("viagens.json","r")
    viagens = json.load(aux)
    return viagens

@app.route('/pontifices', methods=['GET'])
def getPontifices():
    return pontifices

# Rota para obter ranking dos dados
@app.route('/pontifices/top', methods=['GET'])
def getTopPontifices():
    args = request.args
    args = args.to_dict()

    if 'top' in args and 'pontifice' in args:
        # retorna json com o ranking de viagens por ano do pontifice escolhido
        if args['top'] !="" and args['pontifice'] !="":
            js =[]
            lista = viagens['viagens']
            pontifice = args['pontifice']
            # seleciona os anos e insere no set
            intervalo = set()
            for item in lista:
                if item['pontifice'] == pontifice:
                    intervalo.add(item['ano'])
            for ano_viagem in intervalo:
                    data = {"Ano":ano_viagem,"total_viagens":0}
                    js.append(data)
            for data_ano in js:
                    for item in lista:
                        if item['ano'] == data_ano['Ano'] and item['pontifice'] == pontifice:
                            data_ano['total_viagens'] = int(data_ano['total_viagens']) + 1
            js = sorted(js, key=lambda i: i['Ano'],reverse=True)
            return js
    elif 'top' in args:
        # retorna o ranking de viagens por pontifice
        if args['top'] !="":
            top = args['top']
            if top == "viagens":
                js =[]
                lista = viagens['viagens']
                papas=["Francesco","Benedict XVI","John Paul II"]
                for pontifice in papas:
                    count = 0
                    for item in lista:
                        if item['pontifice'] == pontifice:
                            count = count+1
                    data ={"pontifice":pontifice,"total_viagens":count}
                    js.append(data)
                    js = sorted(js, key=lambda i: i['total_viagens'],reverse=True)
            # Retorna ranking de todas as viagens por ano
            elif top == "ano":
                    js =[]
                    lista = viagens['viagens']
                    intervalo = set()
                    for item in lista:
                        intervalo.add(item['ano'])
                    print(intervalo)
                    for ano_viagem in intervalo:
                        data = {"Ano":ano_viagem,"total_viagens":0}
                        js.append(data)
                    for data_ano in js:
                        for item in lista:
                            if item['ano'] == data_ano['Ano']:
                                data_ano['total_viagens'] = int(data_ano['total_viagens']) + 1
                    js = sorted(js, key=lambda i: i['Ano'],reverse=True)
            return js
    return {"msg":"Nenhuma categoria especificada"}

@app.route('/cartas_apostolicas', methods=['GET'])
def getCartasApostolicas():
    return cartas_apostolicas

@app.route('/enciclicas', methods=['GET'])
def getEnciclicas():
    return enciclicas

@app.route('/cartas', methods=['GET'])
def getCartas():
    return cartas

@app.route('/motus', methods=['GET'])
def getMotus():
    return motus

# Rotas para obter dados de viagens por categorias
@app.route('/viagens', methods=['GET'])
def getViagens():
    args = request.args
    args = args.to_dict()
    # Retorna viagens do pontifice no ano especificado 
    if 'pontifice' in args and 'ano' in args:
        if args['pontifice'] !="" and args['ano'] !="":
            pontifice = str (args['pontifice'])
            ano =str( args['ano'])
            js = []
            lista = viagens['viagens']
            for item in lista:
                if item['pontifice'] == pontifice and item['ano']== ano:
                    data = {"id":item['id'],"titulo":item['titulo'],"ano":item['ano'],"pontifice":item['pontifice']}
                    js.append(data)
            return js
        else:
            return {"error":"argumento nulo"}
    # retorna todas as viagens do pontifice
    elif 'pontifice'in args:
        if args['pontifice'] !="":
            pontifice = str (args['pontifice'])
            #print(pontifice)
            js = []
            lista = viagens['viagens']
            for item in lista:
                #print(item)
                if item['pontifice'] == pontifice:
                    data = {"id":item['id'],"titulo":item['titulo'],"ano":item['ano'],"pontifice":item['pontifice']}
                    js.append(data)
        return js
    # Retorna todas as viagens do ano especificado 
    elif 'ano' in args:
        if args['ano'] !="" :
            ano =str( args['ano'])
            js = []
            lista = viagens['viagens']

            for item in lista:
                if item['ano'] == ano:
                    data = {"id":item['id'],"titulo":item['titulo'],"ano":ano,"pontifice":item['pontifice']}
                    js.append(data)
            return js
    return viagens['viagens']

# Rota para contagem do numero de viagens
@app.route('/viagens/contagem', methods=['GET'])
def getContagemViagens():
    # obtem parametros da requisicao e converte para dicionario
    args = request.args
    args = args.to_dict()

    # Retorna a quantidade de viagens realizada pelo pontifice no ano especificado 
    if 'pontifice' in args and 'ano' in args:
        if args['pontifice'] !="" and args['ano'] !="":
            ano = str(args['ano'])
            pontifice = str(args['pontifice'])

            lista = viagens['viagens']
            count =0
            for item in lista:
                if item["ano"] == ano and item["pontifice"] == pontifice:
                    count = count +1
            data = {"total_de_viagens":count,"ano":ano,"pontifice":pontifice}
            return data
    # Retorna a quantidade de viagens realizada pelo pontifice 
    elif 'pontifice' in args:
        if args['pontifice'] !="":
            pontifice = str(args['pontifice'])

            lista = viagens['viagens']
            count =0
            for item in lista:
                if item['pontifice'] == pontifice:
                    count = count+1
            data = {"total_de_viagens":count,"pontifice":pontifice}
            return data
    # Retorna a quantidade de viagens realizada no ano especificado 
    elif 'ano' in args:
         if args['ano']!= "":
            ano = str(args['ano'])

            lista = viagens['viagens']
            count =0
            for item in lista:
                if item['ano'] == ano:
                    count = count+1
            data ={"total_de_viagens":count,"ano":ano}
            return data
    # caso padrão
    # Retorna a quantidade de viagens realizada em todo periodo documentado
    lista = viagens['viagens']
    return {"total_de_viagens":str(len(lista))}

#rotas para obter dados dos destinos das viagens
@app.route('/viagens/destinos', methods=['GET'])
def getDestinos():
    args = request.args
    args = args.to_dict()

    # Retorna os destinos das viagens relaizadas por pontifice e data emque o destino 
    # passado como argumento está na string do destino da viagem
    if 'destino' in args and 'pontifice' in args and 'ano' in args:
         if args['destino'] !="" and args['pontifice'] !="" and args['ano'] !="" :
            destino = str( args['destino'] )
            pontifice = str(args['pontifice'])
            ano = str( args['ano'] )
            lista = viagens['viagens']
            js =[]
            for item in lista:
                # se possuir a string do destino existe uma correspondência
                if destino in str(item['destino']) and item['pontifice'] == pontifice and item['ano'] == ano:
                    data = {"id":item['id'],"destino":item['destino'],"titulo":item['titulo']}
                    js.append(data)
            return js
    # Todas viagens do papa que contem o  destino indicado
    elif 'destino' in args and 'pontifice' in args:
         if args['destino'] !="" and args['pontifice'] !="":
            destino = str( args['destino'] )
            pontifice = str(args['pontifice'])
            lista = viagens['viagens']
            js =[]
            for item in lista:
                # se possuir a string do destino existe uma correspondência
                if destino in str(item['destino']) and item['pontifice'] == pontifice:
                    data = {"id":item['id'],"destino":item['destino'],"titulo":item['titulo'],"ano":item['ano']}
                    js.append(data)
            return js
    #
    # Todas viagens do ano e que contem o destino indicado
    if 'destino' in args and'ano' in args:
         if args['destino'] !="" and args['ano'] !="" :
            destino = str( args['destino'] )
            ano = str( args['ano'] )
            lista = viagens['viagens']
            js =[]
            for item in lista:
                # se possuir a string do destino existe uma correspondência
                if destino in str(item['destino']) and item['ano'] == ano:
                    data = {"id":item['id'],"destino":item['destino'],"titulo":item['titulo'],"pontifice": item['pontifice']}
                    js.append(data)
            return js
    # Retorna a lista dos destinos das viagens por ano do pontifice 
    elif 'pontifice' in args and 'ano' in args:
        if args['pontifice'] !="" and args['ano'] !="" :
            pontifice = str(args['pontifice'])
            ano = str( args['ano'] )
            lista = viagens['viagens']
            js =[]
            for item in lista:
                if (item['pontifice'] == pontifice or item['pontifice']=='all') and item['ano'] == ano:
                    data={"destino":item['destino'],"pontifice":item['pontifice'],"ano":ano,"titulo":item['titulo']}
                    js.append(data)
            return js
    # Retorna a lista dos destinos das viagens do pontifice
    elif 'pontifice' in args:
        if args['pontifice'] !="" :
            pontifice = str(args['pontifice'])

            lista = viagens['viagens']
            js =[]
            for item in lista:
                if item['pontifice'] == pontifice:
                    data={"destino":item['destino'],"ano":item['ano'],"titulo":item['titulo']}
                    js.append(data)
            return js
    # Retorna a lista dos destinos da viagem no ano
    elif 'ano' in args:
        if args['ano'] !="" :
            ano = str( args['ano'] )
            lista = viagens['viagens']
            js =[]

            for item in lista:
                if item['ano'] == ano:
                    data={"destino":item['destino'],"pontifice":item['pontifice'],"titulo":item['titulo']}
                    js.append(data)
            return js
    # Retorna a lista dos destinos que contém a string passada como argumento
    elif 'destino' in args:
        if args['destino'] !="":
            destino = args['destino']
            lista = viagens['viagens']
            js =[]
            for item in lista:
                if destino in str(item['destino']):
                    data = {"id":item['id'],"destino":item['destino'],"titulo":item['titulo'],"pontifice":item['pontifice'],"ano":item['ano']}
                    js.append(data)
            return js
    
    # se não houver qualquer argumento então envia todos destinos
    lista = viagens['viagens']
    js = []
    for item in lista:
        js.append({"destino":str(item['destino']),"titulo":item['titulo'],"ano":item['ano']})
    return js
def main():
    app.run()

if __name__ == '__main__':
    main()
    
