from flask import Flask, send_from_directory, jsonify, request
from multiprocessing import Array, Process, Value
from collections import namedtuple
from ctypes import c_char, c_wchar
from flask_cors import CORS
import threading
import psycopg2
import requests
import time
import json
import os

availableData = []

# ROUTING
app = Flask(__name__, static_folder='static/')
# cors = CORS(app, resources={r"*": {"origins": "*"}})
CORS(app)

@app.route('/')
def root():
    return send_from_directory(os.path.join('.', 'static'), 'index.html')

@app.route('/get')
def API_BASIC():
    return jsonify()

@app.route('/set', methods=['POST'])
def handlePostData():
    exploitableData = None
    try:
        # parsing raw data
        # (?) should look like that: 1,2,3;4,5,6;7,8,9[...]
        rawData = request.data.decode('UTF-8')
        exploitableData = []
        for data in rawData.split(';'):
            subArray = []
            for atomicData in data.split(','):
                subArray.append(atomicData)

            exploitableData.append(subArray)
    except (Exception, psycopg2.Error) as error :
        print(error)
    finally:
        if exploitableData != None:
            availableData = exploitableData
            
        return exploitableData

# start to send asynchronous data
# async_sendSimulationDataToIOT()
    
# main function, simply launching the server
if __name__ == "__main__":
    app.run(debug=True)