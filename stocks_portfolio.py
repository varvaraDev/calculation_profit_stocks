"""Modul for Handling data by stocks portfolio"""
import datetime
from collections import namedtuple

import pandas_datareader.data as web
from pandas_datareader.base import RemoteDataError
import pandas
from calculate import profit_collum, revenue_collum


def parse_str(data):
    """Parsing input values from form.
    Args:
        data (string) data from user
    Return:
        objects StockData for further work
    """
    parse_data = data.split('\r\n')
    parse = [item.split("=") for item in parse_data]
    StockData = namedtuple('StockData', 'stock_id, data_start, revenue')
    try:
        parse_item = [StockData(item[0], item[1], float(item[2]))
                      for item in parse]
    except (TypeError, ValueError, IndexError) as e:
        raise e
    return parse_item


def get_stock2(stock_id, start_date, revenue):
    end = datetime.date.today()
    try:
        start = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        data_stock = web.DataReader(stock_id, 'yahoo', start, end)
    except RemoteDataError as e:
        stock = web.DataReader(stock_id, 'yahoo', start, end)
    except (TypeError, ValueError) as e:
        raise e
    stock = pandas.DataFrame(data_stock.Close)
    stock["profit"] = stock.Close.apply(
        profit_collum,
        args=(stock.Close[0], 1200,)
    )
    stock["revenue"] = stock.Close.apply(
        revenue_collum,
        args=(1200,)
    )
    # Конкатенация года и месяца
    # stock.groupby(pd.TimeGrouper(freq='M')).mean()
    # stock.resample('M').mean()
    return stock.groupby(pandas.TimeGrouper(freq='M')).mean()


def all_stocks_ver1(form):
    StockMonth = namedtuple('StockMonth',
                            'stock_id, stock')
    parse_data = parse_str(form)
    all_stocks = [
        StockMonth(
            stock_id=item.stock_id,
            stock=get_stock2(item.stock_id, item.data_start, item.revenue)
        ) for item in parse_data
    ]
    stocks = pandas.DataFrame({item.stock_id: item.stock.Close
                              for item in all_stocks})
    stocks['period'] = ['{}-{}'.format(str(item.year), str(item.month))
                        for item in stocks.index]
    stocks['total_revenue'] = pandas.DataFrame(
        {item.stock_id: item.stock.revenue for item in all_stocks}
    ).fillna(0).sum(axis=1)
    stocks['total_profit'] = pandas.DataFrame(
        {item.stock_id: item.stock.profit for item in all_stocks}
    ).fillna(0).sum(axis=1)
    return stocks


# id_stocks = [item.stock_id for item in parse]
