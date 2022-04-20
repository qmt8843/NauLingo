from flask import Flask, request
from flask_cors import CORS
from app import translator

app = Flask(__name__)
cors = CORS(app)

app.config['DEBUG'] = True

@app.route("/translate/")
def hello_world():
    try:
        sentence = request.args.get('sentence') #gets 
        output = translator.take_input(sentence)[0] #removes time
        payload = {"sentence":output} #puts in a nice format
        return payload, 200 #OK
    except:
        return "<h1>Bad Request</h1>\nMissing sentence query, or issue with query data", 400 #BAD REQUEST

if __name__ == "__main__":
    # use 0.0.0.0 to use it in container
    app.run(host='0.0.0.0', port=80)