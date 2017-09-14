import datetime
import pandas_datareader.data as web
from pandas_datareader.base import RemoteDataError
from calculate import profit_collum, revenue_collum
from collections import namedtuple


def earnings_stocks(stock_id, start_date, revenue):
    StockHandle = namedtuple('StockData', 'stock_id, data_start, revenue')
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
    month_revenue = new_revenue.resample('M').mean()
    month_profit = profit.resample('M').mean()
    return month_revenue, month_profit


def big_data(parse_item):
    StockAllData = namedtuple('StockAllData', 'stock_id, revenue, profit, date')
    # all_list = [StockAllData(item[0], item[1], item[2]) for item in parse_item]
    all_list = []
    for item in parse_item:
        rev, prof = earnings_stocks(
            item.stock_id,
            item.data_start,
            item.revenue
         )
        date = ['{}-{}'.format(str(item.year),
                str(item.month)) for item in rev.index]
        stock = StockAllData(
            stock_id=item.stock_id,
            revenue=rev,
            profit=prof,
            date=date)
        all_list.append(stock)
    return all_list


def earnings_stocks_test(stock_id, start_date):
    # end_date = format(datetime.date.today(), '%Y-%m-%d')
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
    # print(month_revenue, month_profit)
    return stock.Close

def big_data2(parse_item):
    StockAllData = namedtuple('StockAllData', 'stock_id, revenue, stocke')
    # all_list = [StockAllData(item[0], item[1], item[2]) for item in parse_item]
    all_list = []
    for item in parse_item:
        stock = earnings_stocks_test(
            item.stock_id,
            item.data_start
         )
        frame = StockAllData(
            stock_id=item.stock_id,
            revenue=float(item.revenue),
            stocke=stock)
        all_list.append(frame)
    return all_list
# month = stock.groupby(pandas.Grouper(freq='M')).sum()
# month = stock.groupby(pandas.TimeGrouper(freq='M')).agg(numpy.sum)

# data = 'AAPL=2016-12-24=1200\r\nGOOG=2001-01-01=50\r\nAMZN=2012-01-01=150'
# d1= data.split('\r\n')
# parse = [item.split("=") for item in d1]
# from collections import namedtuple
# StockData = namedtuple('StockData', 'stock_id, data_start, revenue')
# p = StockData('AAPL=2016-12-24=1200'.split("="))
# data2 = [StockData(item[0], item[1], item[2]) for item in parse]
