from flask import Flask

app = Flask(__name__)


@app.route('/21')
def hello_world():  # put application's code here
    return 'Hello World 21!'


if __name__ == '__main__':
    app.run()
