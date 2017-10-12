import tushare as ts

#top = ts.top_list('2017-06-12')

def getStock():
    '''
    GET STOCK HIST DATA
    :return: 
    '''
    stock_data = ts.get_hist_data('600848')[['open','close','low','high']]
    dateData = map(lambda x: x.replace('-','/'),stock_data.index.tolist())
    histData = stock_data.values.tolist()


