import datetime
import numpy
import pandas
import pandas_datareader.data as web
from pandas_datareader.base import RemoteDataError
from calculate import profit_collum, revenue_collum
from collections import namedtuple


def earnings_stocks(stock_id, start_date, revenue):
    StockHandle = namedtuple('StockData', 'stock_id, data_start, revenue')
    revenue = float(revenue)
    end = datetime.date.today()
    try:
        start = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        stock = web.DataReader(stock_id, 'yahoo', start, end)
    except RemoteDataError as e:
        stock = web.DataReader(stock_id, 'yahoo', start, end)
    # except (TypeError, ValueError) as e:
    #     return("""data does not match format '%Y-%m-%d'""")
    # except ValueError as e:
    #     raise e("""data does not match format '%Y-%m-%d'""")
    stock.fillna(method='ffill')
    close = stock.Close
    old_cost = close[0]
    profit = close.apply(profit_collum, args=(old_cost, revenue))
    new_revenue = profit.apply(revenue_collum, args=(revenue,))
    # month2_p = profit.groupby(pandas.Grouper(freq='M'))
    # month2_v = new_revenue.groupby(pandas.Grouper(freq='M'))
    month_revenue = new_revenue.resample('M').mean()
    month_profit = profit.resample('M').mean()
    # return month2_v, month2_p
    return month_revenue, month_profit


# month = stock.groupby(pandas.Grouper(freq='M')).sum()
# month = stock.groupby(pandas.TimeGrouper(freq='M')).agg(numpy.sum)

# data = 'AAPL=2016-12-24=1200\r\nGOOG=2001-01-01=50\r\nAMZN=2012-01-01=150'
# d1= data.split('\r\n')
# parse = [item.split("=") for item in d1]
# from collections import namedtuple
# StockData = namedtuple('StockData', 'stock_id, data_start, revenue')
# p = StockData('AAPL=2016-12-24=1200'.split("="))
# data2 = [StockData(item[0], item[1], item[2]) for item in parse]
