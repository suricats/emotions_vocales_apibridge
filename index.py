from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
from poster.encode import multipart_encode, MultipartParam
from poster.streaminghttp import register_openers
import urllib2
import configenv

app = Flask(__name__)

cors = CORS(app, resources={r"/analyse": {"origins": "*"}})

@app.route('/analyse', methods=['POST'])
@cross_origin(origin='*')
def analyse():
    wav = request.files['wav'].stream.read()
    api_key = request.form['apikey']

    register_openers()
    items = []
    items.append(MultipartParam('apikey', api_key))
    items.append(MultipartParam('wav', wav))
    datagen, headers = multipart_encode(items)
    app.url =  configenv.API_URL
    callRequest = urllib2.Request(app.url, datagen, headers)
    response = urllib2.urlopen(callRequest)

    return(response.read())

if __name__ == '__main__':
   app.run(debug=True)