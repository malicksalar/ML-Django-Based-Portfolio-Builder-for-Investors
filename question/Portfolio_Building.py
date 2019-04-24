import pandas as pd
import numpy as np
from scipy import stats
stock_results=pd.read_csv('stock_results.csv')
market_results=pd.read_csv('market_results.csv')
stock_data=pd.read_csv('stocks_data.csv')
market_data=pd.read_csv('market_data.csv')
ratios=pd.read_csv('PE_RATIOS.csv')
market_data=market_data[-108:]
stock_data=stock_data[-108:]


stock_data=stock_data.drop(['Name'],axis=1)
names=[i for i in stock_data]
market_returns=[j for j in pd.Series([int(i) for i in market_data['KARACHI SE 100 - PRICE INDEX']]).pct_change()][1:]
stock_returns=[]
for nam in stock_data:
    stock_returns.append([j for j in pd.Series([int(i) for i in stock_data[nam] if i>0]).pct_change()][1:])
slopes=[]
for i in stock_returns:
    slopes.append(stats.linregress(market_returns[-len(i):],i).slope)
slopes=[(i*2/3)+0.33 for i in slopes]
market_mean=(sum(market_returns)/len(market_returns))*42
expected_returns=[(0.1108)+(i*(market_mean-0.1108)) for i in slopes]


PE_quartiles=[(ratios['Names'][i],ratios['PE'][i]) for i in range(len(ratios))]
PE_quartiles.sort(key=lambda tup: tup[1])
total=len(PE_quartiles)
PE_Pools=[PE_quartiles[0:int(total/4)],PE_quartiles[int(total/4):int(total/2)],
         PE_quartiles[int(total/2):int(total*3/4)],PE_quartiles[int(-total/4):]]
PE_Pools=[[i[0] for i in j] for j in PE_Pools]



rets={}
for i in range(len(names)):
    rets[names[i]]=expected_returns[i]
Pool_returns=[[rets[j] for j in i] for i in PE_Pools]


# In[29]:


stock_std=[np.std(i) for i in stock_returns]


# In[30]:


stock_stdv={}
for i in range(len(names)):
    stock_stdv[names[i]]=stock_std[i]
Pool_std=[[stock_stdv[j] for j in i] for i in PE_Pools]
comp_Pools=[[(PE_Pools[i][j],Pool_returns[i][j],Pool_returns[i][j]/stock_stdv[PE_Pools[i][j]]) for j in range(len(PE_Pools[i]))]for i in range(len(PE_Pools))]
Final_Pools=[sorted(i, key=lambda tup: (tup[1]) ) for i in comp_Pools]


# In[31]:


pass_names=[[j[0] for j in i] for i in Final_Pools]
pass_exp_returns=[[j[1] for j in i] for i in Final_Pools]
pass_prev_returns=[[stock_returns[i] for i in range(len(names)) if names[i] in k] for k in pass_names]


# In[32]:


def portfolio_builder(stock_names,stock_returns,risk):
    # get adjusted closing prices of 5 selected companies with Quandl
    selected = stock_names
    # calculate daily and annual returns of the stocks
    returns_daily = stock_returns

    ##################
    d=dict(zip(stock_names,stock_returns))
    returns_daily=pd.DataFrame(d)
    returns_annual = returns_daily.mean() *40
    # get daily and covariance of returns of the stock
    cov_daily = returns_daily.cov()
    cov_annual = cov_daily * 45

    # empty lists to store returns, volatility and weights of imiginary portfolios
    port_returns = []
    port_volatility = []
    sharpe_ratio = []
    stock_weights = []

    # set the number of combinations for imaginary portfolios
    num_assets = len(selected)
    num_portfolios = 10000

    #set random seed for reproduction's sake
    np.random.seed(10)

    # populate the empty lists with each portfolios returns,risk and weights
    for single_portfolio in range(num_portfolios):
        weights = np.random.random(num_assets)
        weights /= np.sum(weights)
        returns = np.dot(weights, returns_annual)
        volatility = np.sqrt(np.dot(weights.T, np.dot(cov_annual, weights)))
        sharpe = (returns-0.1108) / volatility
        sharpe_ratio.append(sharpe)
        port_returns.append(returns)
        port_volatility.append(volatility)
        stock_weights.append(weights)

    # a dictionary for Returns and Risk values of each portfolio
    portfolio = {'Returns': port_returns,
                 'Volatility': port_volatility,
                 'Sharpe Ratio': sharpe_ratio}

    # extend original dictionary to accomodate each ticker and weight in the portfolio
    for counter,symbol in enumerate(selected):
        portfolio[symbol+' Weight'] = [Weight[counter] for Weight in stock_weights]

    # make a nice dataframe of the extended dictionary
    df = pd.DataFrame(portfolio)

    # get better labels for desired arrangement of columns
    column_order = ['Returns', 'Volatility', 'Sharpe Ratio'] + [stock+' Weight' for stock in selected]

    # reorder dataframe columns
    df = df[column_order]
    if (risk):
        max_sharp = df['Sharpe Ratio'].max()
        portfolio = df.loc[df['Sharpe Ratio'] == max_sharp]
    else:
        min_vol = df['Volatility'].min()
        portfolio = df.loc[df['Volatility'] == min_vol]
    return portfolio.T


# In[ ]:


def lead_port(weight,portfolio):
    return(weight*portfolio)


# In[ ]:





def port_buils(amount,risk):
    amount=200000
    if amount<=50000:
        divers=[4,3,3,3]
    elif amount<=100000:
        divers=[8,5,3,3]
    elif amount<=150000:
        divers=[10,6,4,4]
    else:
        divers=[14,8,5,4]
    x=2.1

    portfolio_volatility=0
    if x<=2.5:
        port_a=lead_port(0.5,portfolio_builder(pass_names[0][:divers[0]],pass_prev_returns[0][:divers[0]],1))
        port_b=lead_port(0.25,portfolio_builder(pass_names[1][:divers[1]],pass_prev_returns[1][:divers[1]],1))
        port_c=lead_port(0.125,portfolio_builder(pass_names[2][:divers[2]],pass_prev_returns[2][:divers[2]],1))
        port_d=lead_port(0.125,portfolio_builder(pass_names[3][:divers[3]],pass_prev_returns[3][:divers[3]],1))
    elif x<=5:
        port_a=lead_port(1/2,portfolio_builder(pass_names[3][:divers[3]],pass_prev_returns[3][:divers[3]],1))
        port_b=lead_port(1/4,portfolio_builder(pass_names[0][:divers[0]],pass_prev_returns[0][:divers[0]],1))
        port_c=lead_port(1/8,portfolio_builder(pass_names[1][:divers[1]],pass_prev_returns[1][:divers[1]],1))
        port_d=lead_port(1/8,portfolio_builder(pass_names[2][:divers[2]],pass_prev_returns[2][:divers[2]],1))
    elif x<=7.5:
        port_a=lead_port(1/2,portfolio_builder(pass_names[2][:divers[2]],pass_prev_returns[2][:divers[2]],1))
        port_b=lead_port(1/4,portfolio_builder(pass_names[3][:divers[3]],pass_prev_returns[3][:divers[3]],1))
        port_c=lead_port(1/8,portfolio_builder(pass_names[0][:divers[0]],pass_prev_returns[0][:divers[0]],1))
        port_d=lead_port(1/8,portfolio_builder(pass_names[1][:divers[1]],pass_prev_returns[1][:divers[1]],1))
    else:
        port_a=lead_port(1/2,portfolio_builder(pass_names[1][:divers[1]],pass_prev_returns[1][:divers[1]],1))
        port_b=lead_port(1/4,portfolio_builder(pass_names[2][:divers[2]],pass_prev_returns[2][:divers[2]],1))
        port_c=lead_port(1/8,portfolio_builder(pass_names[3][:divers[3]],pass_prev_returns[3][:divers[3]],1))
        port_d=lead_port(1/8,portfolio_builder(pass_names[0][:divers[0]],pass_prev_returns[0][:divers[0]],1))
    port_a.columns=['a']
    port_b.columns=['a']
    port_c.columns=['a']
    port_d.columns=['a']
    final_portfolio = pd.concat([port_a, port_b, port_c, port_d])
    final_portfolio.to_csv('FinalData.csv')
    return final_portfolio
