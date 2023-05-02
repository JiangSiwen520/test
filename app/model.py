from flask import Blueprint
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt 
from statsmodels.tsa.stattools import adfuller # ADF单位根检验
from statsmodels.stats.diagnostic import acorr_ljungbox # 白噪声检验
import statsmodels.api as sm
import itertools
import seaborn as sns

ADF = Blueprint('ADF', __name__)
DIF = Blueprint('DIF', __name__)
WHITE = Blueprint('WHITE', __name__)
ACF_PACF = Blueprint('ACF_PACF', __name__)
AIC_BIC= Blueprint('AIC_BIC', __name__)
PARAM= Blueprint('PARAM', __name__)

# 时序图、ADF
@ADF.route('/ADF')
def fun1():
    series = 'price'
    if series == 'price':
        df = pd.read_excel('000001.xlsx')
    else:
        df = pd.read_excel('new_01.xlsx')
        
    ## 绘制上证指数时间序列图
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams ['axes.unicode_minus'] = False
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.plot(df['date'], df[series], 'k')
    ax.set_title("", fontdict={"fontsize": 15})  # 添加标题，调整字符大小
    ax.set_xlabel("日期",fontdict={"fontsize": 15})  # 添加横轴标签
    ax.set_ylabel(series,fontdict={"fontsize": 15})  # 添加纵轴标签
    ax.tick_params(axis='y',labelsize=15, )# y轴字体大小设置
    ax.tick_params(axis='x',labelsize=15, )# x轴字体大小设置
    plt.savefig("时序图.png")   # 保存图片 注意 在show()之前  不然show会重新创建新的 图片
    plt.show()
    
    ## 平稳性检验
    result = adfuller(df[series].dropna()) #不能拒绝原假设，即原序列存在单位根
    p = result[1].round(4)
     
    return str(p)

# 差分
@DIF.route('/DIF/<int:d>')
def fun2(d):
    df = pd.read_excel('000001.xlsx')
    N = 'dif'+str(d)
    df[N] = df['price'].diff(d)
    df.to_excel('new_01.xlsx')
    
    return {
        'a':'这是新闻模块2！'
        }

# 白噪声
@WHITE.route('/WHITE/<series>')
def fun3(series):
    if series == 'price':
        df = pd.read_excel('000001.xlsx')
    else:
        df = pd.read_excel('new_01.xlsx')
    
    result = acorr_ljungbox(df[series].dropna(), lags = [6,12,18,24]) # 第1行为Ljung-Box统计量 第2行为p值

    return {
        'n':[6,12,18,24],
        'lb_stat':list(result['lb_stat'].values.round(4)),
        'lb_pvalue':list(result['lb_pvalue'].values.round(4)),
        }
 
# ACF、PACF       
@ACF_PACF.route('/ACF_PACF/<series>')
def fun4(series):
    if series == 'price':
        df = pd.read_excel('000001.xlsx')
    else:
        df = pd.read_excel('new_01.xlsx')
    
    fig = plt.figure(figsize=(12,8))
    ax1=fig.add_subplot(211)
    fig = sm.graphics.tsa.plot_acf(df[series].dropna(),lags=20,ax=ax1)
    ax2 = fig.add_subplot(212)
    fig = sm.graphics.tsa.plot_pacf(df[series].dropna(),lags=20,ax=ax2)
    plt.savefig("ACF_PACF.png")

    return 'Y'

# AIC、BIC
@AIC_BIC.route('/AIC_BIC/<series>')
def fun5(series):
    if series == 'price':
        df = pd.read_excel('000001.xlsx')
    else:
        df = pd.read_excel('new_01.xlsx')
        
    p_min=0
    d_min=1
    q_min=0
    p_max=3
    d_max=1
    q_max=3
    results_aic=pd.DataFrame(index=['AR{}'.format(i) for i in range(p_min,p_max+1)],
                           columns=['MA{}'.format(i) for i in range(q_min,q_max+1)])
    results_bic=pd.DataFrame(index=['AR{}'.format(i) for i in range(p_min,p_max+1)],
                           columns=['MA{}'.format(i) for i in range(q_min,q_max+1)])
    for p,d,q in itertools.product(range(p_min,p_max+1),
                                  range(d_min,d_max+1),
                                  range(q_min,q_max+1)):  # 各自排列组合
        if p==0 and d==0 and q==0:
            results_aic.loc['AR{}'.format(p),'MA{}'.format(q)]=np.nan
            results_bic.loc['AR{}'.format(p),'MA{}'.format(q)]=np.nan
            continue
        try:
            model=sm.tsa.ARIMA(df['price'].values,order=(p,d,q))
            results=model.fit()
            results_aic.loc['AR{}'.format(p),'MA{}'.format(q)]=results.aic
            results_bic.loc['AR{}'.format(p),'MA{}'.format(q)]=results.bic
        except:
            continue
        
    results_aic=results_aic.astype(float)
    plt.figure(figsize=(10,8))
    ax=sns.heatmap(results_aic,
                  mask=results_aic.isnull(),
                   annot=True,
                   fmt='.2f'
                  )
    ax.set_title('AIC')
    plt.savefig("AIC.png")
    
    results_bic=results_bic.astype(float)
    plt.figure(figsize=(10,8))
    ax=sns.heatmap(results_bic,
                  mask=results_bic.isnull(),
                   annot=True,
                   fmt='.2f'
                  )
    ax.set_title('BIC')
    plt.savefig("BIC.png")
    
    return 'YY'

# 模型拟合
@PARAM.route('/PARAM/<p>/<d>/<q>')
def fun6(p,d,q):
    if ',' in p:
        p = p.split(',')
        p = [int(x) for x in p]
    else:
        p = int(p)
    if ',' in q:
        q = q.split(',')
        q = [int(x) for x in q] 
    else:
        q = int(q)
    d = int(d)

    df = pd.read_excel('000001.xlsx')
    arma_mod20 = sm.tsa.ARIMA(df['price'].values,order=(p,d,q)).fit()
    res = arma_mod20.resid
    df['res'] = np.hstack((np.full(1, np.nan),res[1:]))
    df['res2'] = df['res']**2
    df.to_excel('new_01.xlsx')
    
    return {
        'AIC':arma_mod20.aic.round(4),
        'BIC':arma_mod20.bic.round(4),
        'ARPARMAS':list(arma_mod20.arparams.round(4)),
        'MAPARAMS':list(arma_mod20.maparams.round(4)),
        'Pvalue':list(arma_mod20.pvalues.round(4)),
        'Tvalues':list(arma_mod20.tvalues.round(4)),
        'p':p
        }
    



