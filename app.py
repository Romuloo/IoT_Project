from flask import Flask, render_template
import json, time, threading
import sys
import Adafruit_DHT


app = Flask(__name__)

alive = 0
data = {}


def tempHumidity():
    data["works"] = False
    while True:
        if data["works"]:
            humidity, temperature = Adafruit_DHT.read_retry(11,4)
            print('Temp:  {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity))
            data["tempHum"] ='Temperature: ' + str(temperature) + ' ºC'  + ' | Humidity: ' + str(humidity) + ' %'
            time.sleep(5)



@app.route('/')
def index():
    return render_template("index.html");


@app.route("/keep_alive", methods=["GET"])
def keep_alive():
    global alive, data
    alive += 1
    keep_alive_count = str(alive)
    data['keep_alive'] = keep_alive_count
    parsed_json = json.dumps(data)
    print(str(parsed_json))
    return str(parsed_json)


@app.route("/status=<name>-<action>", methods = ["POST"])
def event(name, action):
    global data
    print("Got: " + name + ", action: " + action)
    if name == "sensor":
        if action == "ON": 
            data["works"] = True
        elif action == "OFF":
            data["works"] = False
    return str("OK")


if __name__ == '__main__':
    sensorsThread = threading.Thread(target = tempHumidity)
    sensorsThread.start()
    app.run(host = '192.168.1.46', port = 80)

