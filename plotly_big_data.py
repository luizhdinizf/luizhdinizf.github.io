#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 18:34:18 2018

@author: luiz
"""

from sys import getsizeof
import plotly.plotly as py
import cufflinks as cf
import pandas as pd
import numpy as np
import plotly.graph_objs as go
#from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly
plotly.tools.set_credentials_file(username='luizhdinizf', api_key='AMwGYVDfoDhbmJT1TFp7')
plotly.tools.set_config_file(world_readable=True,
                             sharing='public')

filename = '/home/luiz/Fiat/Energy/log.log'      # size 90 GB
def loadfile(filename):
    chunksize = 10**5   
    df_big= pd.read_json(filename, lines=True,chunksize=chunksize)
    df = []
    for chunk in df_big:
        df.append(chunk)
    df = pd.concat(df)
    formata = '%Y-%m-%d %H:%M:%S'
    df['time'] = pd.to_datetime(df['time'],format=formata)
#    df.index=pd.DatetimeIndex(df['time'])

    df.index=df['time']
    df['time'] = str(df['time'])
#    df.drop('time')
    #print(str(getsizeof(df)/1000000)+' Mb')
    return(df)
def resample_and_plot(df,address,interval,mean_interval):
    a = df.loc[df['address'] == address]       
    a=a.resample(interval).mean()    
#    py.plot([{
#        'x': pd.to_datetime(a.index).tolist(),
#        'y': a['decoded_instant'],
#        'name': 'instant'
#        }] ,kind='area', filename='simple-line_'+str(address), fill='tonexty')   
    trace1 = go.Scatter(
    x=pd.to_datetime(a.index).tolist(),
    y=a['decoded_instant'],
    fill='tonexty',
    name='Fluxo de Ar NM³/h'
    )
    cut = a[a.decoded_instant>1]['decoded_instant'].mean()
    std = a[a.decoded_instant>1]['decoded_instant'].std()
    print(std)
    std_high = std/5
    std_low = -std/5
    trace2 = go.Scatter(
    x=pd.to_datetime(a[a.decoded_instant>cut].index).tolist(),
    y=a[a.decoded_instant>cut]['decoded_instant'].rolling(mean_interval).mean()+std_high,
    name='Banda Alta'
    )
    trace3 = go.Scatter(
    x=pd.to_datetime(a[a.decoded_instant>cut].index).tolist(),
    y=a[a.decoded_instant>cut]['decoded_instant'].rolling(mean_interval).mean()+std_low,
    name='Banda Baixa'
    )
    trace4 = go.Scatter(
    x=pd.to_datetime(a[a.decoded_instant>cut].index).tolist(),
    y=a[a.decoded_instant>cut]['decoded_instant'].rolling('1800S').mean(),
    name='Média'
    )
    data = [trace1,trace2,trace3,trace4]
    trechos=[1,2,4,6,8,10]
    layout = dict(title = 'Trecho:'+str(trechos[address-1]),
              yaxis = dict(zeroline = False),
              xaxis = dict(zeroline = False)
             )
    fig = dict(data=data, layout=layout)
#    py.plot(fig, filename='layout'+str(address))
    plotly.offline.plot(fig, filename='trecho'+str(trechos[address-1]))
df = loadfile(filename)
for i in range(1,7):
    resample_and_plot(df,i,'90S','3600S')
    

resample_and_plot(df,2,'90S','3600S')
mean_interval = '4S'
a = df.loc[df['address'] == 2]       
a=a.resample('90S').mean() 
b = a[a.decoded_instant>1]['decoded_instant'].rolling(mean_interval).mean()
#data = [go.Scattergl( x=a.index, y=df['decoded_instant'] )]
#
#
#py.plot(data, filename = 'basic-line', auto_open=True)   
#a.plot(filename='pandas-time-series', auto_open=True)
#py.plot(data, filename='pandas-time-series')
#a.iplot(kind='area', fill=True, filename='cufflinks/stacked-area')
#import datetime

    


#df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv")
#
#
#
#data = [go.Scatter( x=df['Date'], y=df['AAPL.Close'] )]
#
#py.plot(data, filename='pandas-time-series')
#    
#    
#    
#    
#    
#    
#
#total_Mb=getsizeof(df)/1000000
#total_Mb=getsizeof(df)*getsizeof(chunk)/1000000
#
#hdf_fn = 'result.h5'
#hdf_key = 'my_huge_df'
#cols = ['address','decoded_acumulado1','decoded_acumulado2','decoded_instant','time'] # put here a list of all your columns
#cols_to_index = ['time','address'] # put here the list of YOUR columns, that you want to index
#            # you may want to adjust it ... 
#
#store = pd.HDFStore(hdf_fn)
#
#for chunk in a:
#    # don't index data columns in each iteration - we'll do it later
#    store.append(hdf_key, chunk, data_columns=cols_to_index, index=False)
#
## index data columns in HDFStore
#store.create_table_index(hdf_key, columns=cols_to_index, optlevel=9, kind='full')
#store.close()