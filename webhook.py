import json
import os
import requests

from flask import Flask
from flask import request
from flask import make_response

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])

def webhook():
    req = request.get_json(silent=True, force=True)
    print(json.dumps(req, indent=4))

    res = makeResponse(req)
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers["Content-Type"] = "application/json"
    return r

def makeResponse(req):
    result = req.get("queryResult")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    date = parameters.get("date")
    r = requests.get("https://api.openweathermap.org/data/2.5/forecast?q=" + city + "&appid=ed43736919fd647843e9723b61be0e50")
    json_object = r.json()
    weather = json_object["list"]
    
    for i in range(0,30):
        if date in weather[i]["dt_txt"]:
            condition = weather[i]["weather"][0]["description"]
            break

    speech = city + " için " + date + " tarihinde hava durumu " + condition
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