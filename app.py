from flask import Flask, request
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

@app.route('/viagens', methods=['GET'])
def getViagens():
    args = request.args
    args = args.to_dict()
    if 'pontifice' in args and 'ano' in args:
        if args['pontifice'] !="" and args['ano'] !="":
            pontifice = str (args['pontifice'])
            ano =str( args['ano'])
            js = []
            lista = viagens['viagens']
            for item in lista:
                if item['pontifice'] == pontifice and item['ano']== ano:
                    data = {"id":item['id'],"titulo":item['titulo'],"ano":item['ano']}
                    js.append(data)
            return js
        else:
            return {"error":"argumento nulo"}
    elif 'pontifice'in args:
        if args['pontifice'] !="":
            pontifice = str (args['pontifice'])
            #print(pontifice)
            js = []
            lista = viagens['viagens']
            for item in lista:
                #print(item)
                if item['pontifice'] == pontifice:
                    data = {"id":item['id'],"titulo":item['titulo']}
                    js.append(data)
        return js
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
    return viagens

def main():
    app.run()

if __name__ == '__main__':
    main()
    
