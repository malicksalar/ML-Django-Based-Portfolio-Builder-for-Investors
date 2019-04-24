from django.shortcuts import render
from . import forms
import os
from . import models

import pandas as pd
import numpy as np
from scipy import stats

from graphos.sources.simple import SimpleDataSource
from graphos.renderers.gchart import PieChart, AreaChart

stock_results=pd.read_csv('stock_results.csv')
market_results=pd.read_csv('market_results.csv')
stock_data=pd.read_csv('stocks_data.csv')
market_data=pd.read_csv('market_data.csv')
ratios=pd.read_csv('PE_RATIOS.csv')

# Create your views here.

def landing(request):
    return render(request,'landingpage/landing.html')

def about_us(request):
    return render(request,'aboutpage/about.html')

def display(request):
    posts = list(models.form_data.objects.all().values_list('name', 'value'))
    posts = [list(a) for a in posts]
    # Chart object
    end_table_data = []
    value_of_bonds = posts[-4][1]
    value_of_return = posts[-3][1]
    value_of_volatility = posts[-2][1]
    value_of_amount = posts[-1][1]

    volatility_per = posts[-2]
    returns_per = posts[-3]

    posts = posts[0:-3]

    first_graph_data = posts


    for x in range(len(first_graph_data)):
        if(x < len(first_graph_data) - 1):
            first_graph_data[x][1] = first_graph_data[x][1] * (1 - value_of_bonds)

    first_graph_data.insert(0,['Companies','Values'])

    data_source = SimpleDataSource(data=first_graph_data)

    chart1 = PieChart(data_source, html_id='piechart_id', options={'pieHole' : 0.4, 'title': 'Percentage to invest'})


    now = []
    if_high = []
    if_low = []
    expected = []
    area_graph = []


    for x in range(0,13):
        now.append(value_of_amount)

    for x in range(0,13):
        xxx = (value_of_bonds * value_of_amount)
        xxx = xxx + (xxx * 0.1108)
        xx = ((1 - value_of_bonds) * value_of_amount)
        xx = xx + (((value_of_return + value_of_volatility)/12) * x * xx)
        if_high.append(xx + xxx)

    for x in range(0,13):
        xxx = (value_of_bonds * value_of_amount)
        xxx = xxx + (xxx * 0.1108)
        xx = ((1 - value_of_bonds) * value_of_amount)
        xx = xx + (((value_of_return - value_of_volatility)/12) * x * xx)
        if_low.append(xx + xxx)

    for x in range(0,13):
        xxx = (value_of_bonds * value_of_amount)
        xxx = xxx + (xxx * 0.1108)
        xx = ((1 - value_of_bonds) * value_of_amount)
        xx = xx + (((value_of_return)/12) * x * xx)
        expected.append(xx + xxx)



    for i in range(0,13):
        if (i == 0):
            area_graph.append(['Month','Saved','Max Profit','Min Profit','Expected Profit'])
        else:
            area_graph.append([i, now[i], if_high[i], if_low[i], expected[i]])



    data_source1 = SimpleDataSource(data=area_graph)


    chart2 = AreaChart(data_source1,html_id='piechart_id2', options={'title': 'Future Projections'})


    end_table_data = list(first_graph_data)
    end_table_data = end_table_data[1:]
    end_table_data.insert(0, [returns_per[0], returns_per[1] * 100])
    end_table_data.insert(0, [volatility_per[0], volatility_per[1] * 100])


    for x in range(len(end_table_data)):
        if (x < 2):
            end_table_data[x] = end_table_data[x][0] + '  -  ' + str(int(end_table_data[x][1])) + ' %'
        else:
            end_table_data[x] = end_table_data[x][0] + '  -  ' + 'Rs ' + str(int(end_table_data[x][1] * value_of_amount))


    context = {'Portfolio': chart1 , 'Data' : chart2, 'End': end_table_data}

    return render(request,'displaypage/graphs.html', context)


def form_name_view(request):
    form = forms.formName()

    if request.method == 'POST':
        form = forms.formName(request.POST)


        if form.is_valid():
            print("Success")
            print('Q1: '+ form.cleaned_data['name1'])
            print('Q2: '+ form.cleaned_data['name2'])
            print('Q3: '+ form.cleaned_data['name3'])
            print('Q4: '+ form.cleaned_data['name4'])
            print('Q5: '+ form.cleaned_data['name5'])
            print('Q6: '+ form.cleaned_data['name6'])
            print('Q7: '+ form.cleaned_data['name7'])
            print('Q8: '+ form.cleaned_data['name8'])
            amount_to_invest = int(form.cleaned_data['name9'])

            avg = int(form.cleaned_data['name1'])+int(form.cleaned_data['name2'])+int(form.cleaned_data['name3'])+int(form.cleaned_data['name4'])+int(form.cleaned_data['name5'])+int(form.cleaned_data['name6'])+int(form.cleaned_data['name7'])+int(form.cleaned_data['name8'])
            avg = avg/8
            avg = (avg/6) * 10
            print("The risk score is : ",avg)

            models.form_data.objects.all().delete()

            data_got = port_buils(amount_to_invest,avg)


            comp_names = list(data_got['Companies'])
            comp_values = list(data_got['Portfolio'])
            for x in range(len(comp_names)):
                post = models.form_data()
                post.name = comp_names[x]
                post.value = comp_values[x]
                post.save()


    return render(request,'formpage/form_page.html',{'form':form})


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
        portfolio[symbol+' '] = [Weight[counter] for Weight in stock_weights]

    # make a nice dataframe of the extended dictionary
    df = pd.DataFrame(portfolio)

    # get better labels for desired arrangement of columns
    column_order = ['Returns', 'Volatility', 'Sharpe Ratio'] + [stock+' ' for stock in selected]

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
    if amount<=50000:
        divers=[4,3,3,3]
    elif amount<=100000:
        divers=[8,5,3,3]
    elif amount<=150000:
        divers=[10,6,4,4]
    else:
        divers=[14,8,5,4]
    bonds = 0
    x = risk
    portfolio_volatility=0
    if x<=2.5:
        port_a=lead_port(0.5,portfolio_builder(pass_names[0][:divers[0]],pass_prev_returns[0][:divers[0]],1))
        port_b=lead_port(0.25,portfolio_builder(pass_names[1][:divers[1]],pass_prev_returns[1][:divers[1]],1))
        port_c=lead_port(0.125,portfolio_builder(pass_names[2][:divers[2]],pass_prev_returns[2][:divers[2]],1))
        port_d=lead_port(0.125,portfolio_builder(pass_names[3][:divers[3]],pass_prev_returns[3][:divers[3]],1))
        bonds = 0.3

    elif x<=5:
        port_a=lead_port(1/2,portfolio_builder(pass_names[3][:divers[3]],pass_prev_returns[3][:divers[3]],1))
        port_b=lead_port(1/4,portfolio_builder(pass_names[0][:divers[0]],pass_prev_returns[0][:divers[0]],1))
        port_c=lead_port(1/8,portfolio_builder(pass_names[1][:divers[1]],pass_prev_returns[1][:divers[1]],1))
        port_d=lead_port(1/8,portfolio_builder(pass_names[2][:divers[2]],pass_prev_returns[2][:divers[2]],1))
        bonds = 0.25
    elif x<=7.5:
        port_a=lead_port(1/2,portfolio_builder(pass_names[2][:divers[2]],pass_prev_returns[2][:divers[2]],1))
        port_b=lead_port(1/4,portfolio_builder(pass_names[3][:divers[3]],pass_prev_returns[3][:divers[3]],1))
        port_c=lead_port(1/8,portfolio_builder(pass_names[0][:divers[0]],pass_prev_returns[0][:divers[0]],1))
        port_d=lead_port(1/8,portfolio_builder(pass_names[1][:divers[1]],pass_prev_returns[1][:divers[1]],1))
        bonds = 0.2
    else:
        port_a=lead_port(1/2,portfolio_builder(pass_names[1][:divers[1]],pass_prev_returns[1][:divers[1]],1))
        port_b=lead_port(1/4,portfolio_builder(pass_names[2][:divers[2]],pass_prev_returns[2][:divers[2]],1))
        port_c=lead_port(1/8,portfolio_builder(pass_names[3][:divers[3]],pass_prev_returns[3][:divers[3]],1))
        port_d=lead_port(1/8,portfolio_builder(pass_names[0][:divers[0]],pass_prev_returns[0][:divers[0]],1))
        bonds = 0.1
    port_a.columns=['a']
    port_b.columns=['a']
    port_c.columns=['a']
    port_d.columns=['a']
    final_portfolio = pd.concat([port_a, port_b, port_c, port_d])
    indices = list(final_portfolio.index.values)
    values = list(final_portfolio['a'])

    total_return = 0
    total_volatility = 0
    for a in range(len(values)):
        if (str(indices[a]) == 'Returns'):
            total_return = total_return + values[a]
            indices[a] = 0
            values[a] = 0
        elif (str(indices[a]) == 'Sharpe Ratio'):
            indices[a] = 0
            values[a] = 0
        elif (str(indices[a]) == 'Volatility'):
            total_volatility = total_volatility + values[a]
            indices[a] = 0
            values[a] = 0

    indices = list(filter(lambda a: a != 0, indices))
    values = list(filter(lambda a: a != 0, values))
    indices.append('Bonds')
    values.append(bonds)
    indices.append('Return')
    indices.append('Volatility')
    values.append(total_return)
    values.append(total_volatility)
    indices.append('Amount')
    values.append(amount)

    final_portfolio = pd.DataFrame()
    final_portfolio['Companies'] = indices
    final_portfolio['Portfolio'] = values


    final_portfolio.to_excel('static/displaypage/FinalData.xlsx', index = None)
    return final_portfolio
