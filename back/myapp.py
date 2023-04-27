# from asyncio.windows_events import NULL
from flask import Flask
from flask_cors import CORS
from flask import request
# import pandas as pd
# import numpy as np
from word_counts import word_count
from sentiment import senti_analysis
from EventExtraction import openie2triple
from sentence_filt_by_time import sentence_filt_by_time
from convert2df import list2df
from RumorTree import rumor_analysis
# import json
import os
os.chdir("/data-14T/zhangyixing/SocialComputing/Social_Computing/back")
app = Flask(__name__)
cors = CORS(app, resources={"/api/*": {"origins": "*"}})

@app.route('/api/convert2df', methods=["GET","POST"])
def convert2df():
    print(request)
    if request.method == 'POST':
        req_data = request.get_json()
        # print(req_data)
        res = list2df(req_data["list"])
        print("static_res")
        print(res)
        return {"res":res}
    else:
        return {}

@app.route('/api/words', methods=["GET","POST"])
def words_count():
    print(request)
    if request.method == 'POST':
        req_data = request.get_json()
        print(req_data)
        res = word_count(req_data["start"],req_data["end"],req_data["thresh"])
        
        return {"res":res}
    else:
        return {}
@app.route('/api/sentiment', methods=["GET","POST"])
def sentiment():
    print(request)
    if request.method == 'POST':
        req_data = request.get_json()
        print("req_data********************************************")
        print(req_data)
        res = senti_analysis(req_data["start"],req_data["end"],req_data["event"],req_data["day_or_year"],req_data["proportion"])
        
        return {"res":res}
    else:
        return {}


@app.route('/api/RumorTree', methods=["GET","POST"])
def RumorTree():
    # print(request)
    if request.method == 'POST':
        req_data = request.get_json()
        res = rumor_analysis(req_data["date"],req_data["event"])
        print("req_res********************************************")
        # print(res)
        return res
    else:
        return {}


@app.route('/api/textlist', methods=["GET","POST"])
def textlist():
    print(request)
    if request.method == 'POST':
        req_data = request.get_json()
        print("req_data********************************************")
        print(req_data)
        res = sentence_filt_by_time(req_data["date"],req_data["event"])
        
        return {"res":res}
    else:
        return {}

@app.route('/api/EventExtraction', methods=["GET","POST"])
def EventExtraction():
    print(request)
    if request.method == 'POST':
        req_data = request.get_json()
        print("req_data********************************************")
        print(req_data)
        res = openie2triple(req_data["content"])
        
        return {"res":res}
    else:
        return {}
# class Hello(Resource):
#     @staticmethod
#     def get():
#         return "[get] hello flask"

#     @staticmethod
#     def post():
#         return "[post] hello flask"


# api.add_resource(Hello, '/hello')

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=9931 )
