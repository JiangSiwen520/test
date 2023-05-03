from flask import Flask
import os


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
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 80)))
