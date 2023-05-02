import os

from flask import Flask
import model
import pandas as pd
from statsmodels.tsa.stattools import adfuller # ADF单位根检验

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, Welcome to CloudBase!13:4\n'



# 将 model 模块里的蓝图对象 new_list 注册到 app
# app.register_blueprint(model.ADF)

if __name__ == "__main__":
    #app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
    app.run(host='0.0.0.0', debug=True, port=80)


