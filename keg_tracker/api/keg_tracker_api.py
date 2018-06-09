from flask import Flask, Request, render_template, jsonify, redirect
import flask_login
from keg_tracker.config import ConfigDict
import os
from pathlib import Path

conf_dict = ConfigDict().conf_dict

config_path = '../config.py'
app = Flask(__name__, instance_relative_config=False)
app.config.from_pyfile(config_path)

@app.route('/', methods=['GET'])
def main_reroute():
    return redirect('index.html')

@app.route('/index.html', methods=['GET'])
def index_html():
    p = Path('/sys/bus/w1/devices/')
    sensor_dir = ''
    for entry in p.iterdir():
        if '28-' in str(entry):
            sensor_dir = str(entry)
    if sensor_dir is not '':
        with open(f"{sensor_dir}/w1_slave", mode='r') as temp_file:
            temp_str = str(temp_file.read())
        temp = int(float(temp_str.split('t=')[1].replace('\n', '')) / 1000) * 9/5 + 32
    return render_template('index.html', flask=f'Temp is {temp} degrees F')

@app.route('/setup_keg.html', methods=['GET'])
def setup_keg():
    return render_template('setup_keg.html')

def main():
    HOST = os.getenv('SERVER_HOST', '0.0.0.0')
    PORT = int(conf_dict['server_port'])
    THREADED = app.config['THREADED']
    PROCESSES = app.config['PROCESSES']
    FLASK_DEBUG = app.config['FLASK_DEBUG']
    if app.config['USE_SSL']:
        app.run(debug=FLASK_DEBUG, host=HOST, port=PORT,
                threaded=THREADED,
                processes=PROCESSES,
                ssl_context=('server.crt', 'server.key'))
    else:
        app.run(debug=FLASK_DEBUG,
                host=HOST,
                port=PORT,
                threaded=THREADED,
                processes=PROCESSES)


if '__main__' == __name__:
    print(type(conf_dict))
    main()