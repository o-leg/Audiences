__version__ = '0.1.0'

from flask import Flask, Response

from auth import auth
from Functions.user import user
from Functions.audience import audience
from Functions.reservation import reservation

app = Flask(__name__)
app.register_blueprint(auth)
app.register_blueprint(user)
app.register_blueprint(audience)
app.register_blueprint(reservation)


@app.route('/api/v1/hello-world-7')
def myendpoint():
    status_code = Response(response="Hello World 7")
    return status_code

if __name__ == '__main__':
    app.run(debug=True, port=2012)
