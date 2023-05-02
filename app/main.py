import os

from flask import Flask
import model

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, Welcome to CloudBase_JSW, 2023-02-13!!!->2023.5.1\n'

# 将 model 模块里的蓝图对象 new_list 注册到 app
app.register_blueprint(model.ADF)
app.register_blueprint(model.DIF)
app.register_blueprint(model.WHITE)
app.register_blueprint(model.ACF_PACF)
app.register_blueprint(model.AIC_BIC)
app.register_blueprint(model.PARAM)

if __name__ == "__main__":
    #app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
    app.run(host='0.0.0.0',debug=True, port=80)
