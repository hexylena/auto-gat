from flask import Flask
from flask import request
import subprocess
import copy

app = Flask(__name__)

default_args = {
    'theme': 'solarized-light',
    'speed': '1',
    'scale': '2',
    'columns': '80',
    'rows': '20',
}

@app.route("/", methods=['GET', 'POST'])
def index():
    args = copy.copy(default_args)
    args.update(request.args)
    subprocess.check_call([
        '/app/asciicast2mp4',
        '-t', args['theme'],
        '-s', args['speed'],
        '-S', args['scale'],
        '-w', args['columns'],
        '-h', args['rows'],
        '/data/1.cast',
    ])
    return "Done!"
