import tushare as ts
import pandas as pd
#top = ts.top_list('2017-06-12')

def getStock(name='sh'):
    '''
    GET STOCK HIST DATA
    :return: 
    '''
    # get stock data
    stock_data = ts.get_hist_data(name)[['open','close','low','high']]

    # sort by date
    stock_data.index = pd.to_datetime(stock_data.index)
    stock_data = stock_data.sort_index(axis=0, ascending=True)

    # process date
    #stock_data.index = map(lambda x: x.strftime('%Y-%m-%d'), stock_data.index)
    #dateData = map(lambda x: x.replace('-','/'),stock_data.index.tolist())
    stock_data['date'] = map(lambda x: x.strftime('%Y-%m-%d'), stock_data.index)
    stock_data['date'] = stock_data['date'].apply(lambda x: x.replace('-', '/'))
    stockData = stock_data[['date', 'open', 'close', 'low', 'high']]

    #histData = stock_data.values.tolist()
    #return dateData,histData
    return stockData.values.tolist()

