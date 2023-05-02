from flask import Flask
import pandas as pd

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, Welcome to CloudBase!35\n'
@app.route('/ne')
def fun2():
    q = 4
    return {
        'p':q,
        'name':2333
        }


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False, port=5000)
