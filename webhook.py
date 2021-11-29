import json
import os
import requests

from flask import Flask
from flask import request
from flask import make_response

app = Flask(__name__)
api_key = 'ed43736919fd647843e9723b61be0e50'

@app.route('/webhook', methods=['POST'])

def webhook():
    req = request.get_data().decode('utf-8')
    req = json.loads(req)
    res = makeResponse(req)
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeResponse(req):
    result = req.get("queryResult")
    parameters = result.get("parameters")
    city = parameters.get("city")
    date = parameters.get("date")[:10]
    url_ = str('http://api.openweathermap.org/data/2.5/forecast?q=' + str(city) + '&appid=' + str(api_key))
    r = requests.get(url_)
    json_object = r.json()
    weather = json_object["list"]
    
    for i in range(0,30):
        if date in weather[i]["dt_txt"]:
            condition = weather[i]["weather"][0]["description"]
            break

    speech = city + " şehrinde " + date + " tarihinde hava durumu " + condition
    return {
        "fulfillmentText": speech
        # "speech": speech,
        # "displayText": speech,
        # "source": "Webhook"
    }


if __name__== "__main__":
    port = int(os.getenv("PORT", 5000))
    print("starting app on port %d" % port)
    app.run(debug=False, port=port, host="0.0.0.0")