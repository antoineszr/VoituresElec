from spyne import *
from spyne.server.wsgi import WsgiApplication
from spyne.protocol.soap import Soap11
from spyne import *
from math import sin, cos, acos, pi
import requests
import json
# import os
# from flask import Flask

# app = Flask(__name__)

class tempsParcours(ServiceBase):
    @rpc(String, String, String, String, String, _returns=String)
    def tempsParcours(ctx, latA, longA, latB, longB, autonomie):
        proto="http://wxs.ign.fr/essentiels/itineraire/rest/route.json?origin=" + latA + "," + longA + "&destination=" + latB + "," + longB + "&method=DISTANCE&graphName=Voiture"
        rawdata= requests.get(proto)
        json_loaded = rawdata.json()
        duration = json_loaded.get('duration')
        distance = json_loaded.get('distance')

        print("distance = " + distance)
        print("autaunomie = " + autonomie)

        if distance > autonomie:
            result = "Une recharge sera nécessaire en plus du trajet d'une durée de " + duration
        else:
            result = "trajet d'une durée de " + duration
        return result

            
application = Application([tempsParcours], 'spyne.examples.hello.soap', in_protocol=Soap11(validator='lxml'), out_protocol=Soap11())
wsgi_application = WsgiApplication(application)

# @app.route("/")
# def hello():
#     return wsgi_application



if __name__ == "__main__":
    # port = int(os.environ.get("PORT", 5000))
    # app.run(host='127.0.0.1', port=port)


    from wsgiref.simple_server import make_server
    server = make_server('0.0.0.0', 80, wsgi_application)
    server.serve_forever()