from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
from poster.encode import multipart_encode, MultipartParam
from poster.streaminghttp import register_openers
import urllib2

app = Flask(__name__)

cors = CORS(app, resources={r"/analyse": {"origins": "*"}})

@app.route('/analyse', methods=['POST'])
@cross_origin(origin='*')
def analyse():
    wav = request.files['wav'].stream.read()
    api_key = request.form['apikey']

    url="https://api.webempath.net/v2/analyzeWav"
    register_openers()
    items = []
    items.append(MultipartParam('apikey', api_key))
    items.append(MultipartParam('wav', wav))
    datagen, headers = multipart_encode(items)
    callRequest = urllib2.Request(url, datagen, headers)
    response = urllib2.urlopen(callRequest)

    if response.getcode() == 200:
        return(response.read())
    else:
        return(response.read())

    return 'Something went wrong'

if __name__ == '__main__':
   app.run(debug=True)