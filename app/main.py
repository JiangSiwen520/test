import os

from flask import Flask
import pandas as pd
from statsmodels.tsa.stattools import adfuller # ADF单位根检验

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, Welcome to CloudBase!35\n'
@app.route('/ADF')
def fun2():
    
    df = pd.read_excel('000001.xlsx')
    result = adfuller(df['price'].dropna()) #不能拒绝原假设，即原序列存在单位根
    p = result[1].round(4)
    q = 4
    return {
        'p':p
        }


if __name__ == "__main__":
    #app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
    app.run(host='0.0.0.0', debug=False, port=3000)
