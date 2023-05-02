import os

from flask import Flask
import model

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, Welcome to CloudBase_JSW, 2023-02-13!!!->2023.5.1\n'

if __name__ == "__main__":
    #app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
    app.run(host='0.0.0.0',port=80)
