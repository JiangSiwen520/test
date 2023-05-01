import os

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    import pandas as pd
    #df = pd.read_excel('000001.xlsx')
    #a = df.columns[0]
    b = 'date'
    return 'Hello, Welcome to CloudBase_JSW, 2023-02-13!!!->5.1\n'+b+a

if __name__ == "__main__":
    #app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
    app.run(host='0.0.0.0', debug=True, port=80)
