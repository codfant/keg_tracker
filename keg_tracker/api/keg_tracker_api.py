from flask import Flask, Request, render_template, jsonify, redirect
from keg_tracker.config import ConfigDict
import os
import pyqrcode



conf_dict = ConfigDict().conf_dict
config_path = '../config.py'
app = Flask(__name__, instance_relative_config=False)
app.config.from_pyfile(config_path)


@app.route('/', methods=['GET'])
def main_reroute():
    return redirect('index.html')


@app.route('/index.html', methods=['GET'])
def index_html():
        return render_template('index.html', flask=f'Temp sensor not found.')


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
    url = pyqrcode.create(conf_dict['site_url'])
    url.svg('./static/img/qr_code.svg', scale=8)
    main()