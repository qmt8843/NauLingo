import translator
from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import logging

#Setup logging config
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', encoding='utf-8', level=logging.DEBUG, handlers=[
        logging.FileHandler("data\\bot.log"),
        logging.StreamHandler()
        ])

app = Flask(__name__)
api = Api(app)
cors = CORS(app)

#Setup required arguments for translator
parser = reqparse.RequestParser()
parser.add_argument('sentence', required=True, type=str, help="Sentence cannot be blank!")

#Translator page
class Translator(Resource):
    #Gives sentence, gets translation
    def get(self):
        args = parser.parse_args()
        output = translator.take_input(args["sentence"])[0] #removes time
        payload = {"sentence":output} #puts in a nice format
        return payload, 200 #OK

#Translator resource
api.add_resource(Translator, "/translate/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=443, debug=True, ssl_context=('data\\cert.pem', 'data\\privkey.pem'))