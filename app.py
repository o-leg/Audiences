__version__ = '0.1.0'

from flask import Flask, Response
from waitress import serve

from auth import auth
from user import user
from audience import audience
from reservation import reservation

app1 = Flask(__name__)
app1.register_blueprint(auth)
app1.register_blueprint(user)
app1.register_blueprint(audience)
app1.register_blueprint(reservation)


@app1.route('/api/v1/hello-world-7')
def myendpoint():
    status_code = Response(response="Hello World 7")
    return status_code

serve(app1, host='0.0.0.0', port=8089, threads=1)
