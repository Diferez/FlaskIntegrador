from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
from statistics import mode

app = Flask('__name__')
CORS(app)

tipo_medicion = {'sensor':'FC28','variable':'Humedad','unidades':'% agua por volumen de tierra'}  #Ejemplo para el ph

medicion = [
    {'fecha':'2019-06-20 11:24:06',**tipo_medicion,'valor':70, 'id':1},
    {'fecha':'2019-05-20 11:24:06',**tipo_medicion,'valor':25, 'id':2},
    {'fecha':'2019-04-20 11:24:06',**tipo_medicion,'valor':25, 'id':3}
]
iden = 4

@app.route('/mediciones',methods=['POST'])
def postMediciones():
    global iden
    now = datetime.now()
    body = request.json
    body['fecha'] = datetime.strftime(now, '%Y-%m-%d %H:%M:%S')
    body['id'] = iden
    iden = iden + 1
    medicion.append({**body,**tipo_medicion})
    return jsonify(medicion)

@app.route('/mediciones',methods=['GET'])
def getAll():
    return jsonify(medicion)

@app.route('/moda',methods=['GET'])
def getModa():
    m = []
    for x in medicion:
        m.append(x['valor'])
    try:
        m = mode(m) 
    except:
        return jsonify(valor = None)

    return jsonify(valor = m)

@app.route('/mediciones',methods=['DELETE'])
def delete():
    body = request.json
    ide = body['id']
    for x in range(0,len(medicion)-1):
        if (medicion[x]['id']==ide):
            medicion.remove(medicion[x])
    return jsonify(medicion)

@app.route('/mediciones',methods=['PUT'])
def puts():

    now = datetime.now()
    body = request.json
    body['fecha'] = datetime.strftime(now, '%Y-%m-%d %H:%M:%S')
    ide = body['id']
    for x in range(0,len(medicion)-1):
        if (medicion[x]['id']==ide):
            medicion[x]['valor'] = body['valor']
            medicion[x]['fecha'] = body['fecha']
            return jsonify(medicion)
    
    medicion.append({**body,**tipo_medicion})
    return jsonify(medicion)
 

@app.route('/')
def test():
    return "Welcome"

 


app.run(port=8080,debug=True)