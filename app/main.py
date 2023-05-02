from flask import Flask
import model
import pandas as pd

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, Welcome to CloudBase!35\n'
@app.route('/ne')
def fun2():
    q = 4
    df = pd.read_excel('000001.xlsx')
    name = pd.columns[0]
    return {
        'p':q,
        'name':name
        }


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False, port=80)
