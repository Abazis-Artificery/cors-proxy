# Originally created by Abazis Artificery LLC
# MIT License. 
# Hope it's as useful for you as it has been for me
#   Simply parses out a http request that is arbitrarily json-ified an incoming POST's data field, and forwards it along.
#   Then parses out the response to that http request, and passes it back in the original POST request's data, following another arbitary format. 

import threading 
import requests
import ast
import base64
import json

from flask import Flask, request, Response, jsonify
from flask_cors import CORS
from waitress import serve

# Create our Flask App object
app = Flask(__name__)

#Enable CORS support for our flask app object
CORS(app)

#Define what happens at our root route
@app.route("/", methods=['POST'])
def root_handle_all():
    match request.method:
        case 'POST':
            try:
                data = request.get_json()
                googleResponse=requests.request(
                        method=data['method'], 
                        url=data['url'],
                        data=base64.b64decode(data['data']) if 'data' in data else None,
                        headers = data['headers'] if 'headers' in data else None
                    )
                responseData={
                    "data": base64.b64encode(googleResponse.content).decode(),
                    "status": googleResponse.status_code,
                    "headers": dict(googleResponse.headers),
                }
                return(jsonify(responseData))
            except KeyError as e:
                return(str(e), 400)
        case _:
              return("Success. Sorta.")
#Serve our flask object
HOST = "0.0.0.0"
PORT = "8080"
server_thread = threading.Thread(
    target=serve, 
    args=(app,), 
    kwargs={'host':HOST, 'port':PORT}
)

#Start the server thread
server_thread.start()

#Wait for the server thread to terminate (hopefully terminates never!)
server_thread.join()
