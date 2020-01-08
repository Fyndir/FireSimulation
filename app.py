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

# the data you can access via /get and set the value through /set
global availableData
availableData = []


# ---------------------------------------------------------------------------------------------
# @brief
#  Returns True if 'stringo' is an integer or a float, Flase otherwise
def isStringIntOrFloat(stringo):
    if stringo.isdigit():
        return True
    if stringo.replace('.', '', 1).isdigit() and stringo.count('.') < 2:
        return True
    return False

# ROUTING
app = Flask(__name__, static_folder='static/')
# cors = CORS(app, resources={r"*": {"origins": "*"}})
CORS(app)

@app.route('/')
def root():
    return send_from_directory(os.path.join('.', 'static'), 'index.html')

@app.route('/get')
def API_BASIC():
    return jsonify(availableData)

@app.route('/send', methods=['POST'])
def handlePostData():
    global availableData
    exploitableData = None
    rawData = ''

    # parsing received data
    # (?) should look like that: 1,2,3;4,5,6;7,8,9[...]
    try:
        rawData = request.data.decode('UTF-8')
        exploitableData = []

        # if there was no delimiter (aka on a envoyé qu'un seul triplet)
        splittedData = rawData.split(';')
        if splittedData[0] == rawData:
            subArray = []
            for atomicData in splittedData[0].split(','):
                if len(atomicData) > 0 and isStringIntOrFloat(atomicData):
                    subArray.append(atomicData)

            # array integrity check
            if (len(subArray) == 3):
                exploitableData.append(subArray)

        # sinon, on a envoyé plusieurs triplets, donc simplement faut les traiter un par un
        else:
            print('envoyé plusieurs triplets')
            for data in rawData.split(';'):
                subArray = []
                for atomicData in data.split(','):
                    if len(atomicData) > 0 and isStringIntOrFloat(atomicData):
                        subArray.append(atomicData)

                # array integrity check
                if (len(subArray) == 3):
                    exploitableData.append(subArray)
                else :
                    raise NameError('Mauvais typage')
    except (Exception, psycopg2.Error) as error :
        print(error)
        exploitableData = None
    finally:
        if exploitableData != None:
            availableData = exploitableData
            stringifiedArray = ''.join(str(x) for x in exploitableData)
            return stringifiedArray
        else:
            return 'no data'

# start to send asynchronous data
# async_sendSimulationDataToIOT()
    
# main function, simply launching the server
if __name__ == "__main__":
    app.run(debug=True)
