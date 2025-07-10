import threading 
import requests
from flask import Flask, request, Response, abort
from flask_cors import CORS
from waitress import serve

# Create our Flask App object
app = Flask(__name__)

#Enable CORS support for our flask app object
CORS(app)

#Define what a "get" request to our flask object does
@app.route("/")
def root_handle_all():
    try:
        targetUrl = request.headers["Target-Url"]
        target_headers = {key:value for key, value in request.headers.items() if (key!="Target-Url") and (key!="Host")}
        proxyRequest=requests.Request(
            method=request.method, 
            url=targetUrl,
            headers=target_headers,
            data=request.data
        )
    except KeyError:
        return("Target-Url header missing.", 400)
    response = requests.Session().send(proxyRequest.prepare())
    return( 
        response.content,
        response.status_code, 
        response.headers
    )

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
