from flask import Flask, render_template
import json, time, threading

app = Flask(__name__)

alive = 0
data = {} 


@app.route('/')
def index():
    return render_template("index.html");

@app.route('/keep_alive', methods=["GET"])
def keep_alive():
    global alive, data
    alive += 1
    keep_alive_count = str(alive)
    data['keep_alive'] = keep_alive_count
    parsed_json = json.dumps(data)
    print(str(parsed_json))
    return str(parsed_json)


if __name__ == '__main__':
    app.run(host = '192.168.1.46',port=80)

