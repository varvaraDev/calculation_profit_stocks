"""Modul for Handling data by stocks portfolio"""
import datetime
from collections import namedtuple

import pandas_datareader.data as web
from pandas_datareader.base import RemoteDataError
import pandas
from handle_exceptions import RequestError
import numpy as np


def parse_form(data):
    """Parsing input values from form.
    Args:
        data (string) data from forb by get requsest
    Return:
        objects StockData for get data about stock
    """
    parse_data = data.split('\r\n')
    parse = [item.split("=") for item in parse_data]
    StockData = namedtuple('StockData', 'stock_id, data_start, revenue')
    try:
        parse_item = [StockData(item[0], item[1], float(item[2]))
                      for item in parse]
    except (TypeError, ValueError, IndexError, AttributeError) as e:
        raise RequestError(e)
    return parse_item


def get_final_frame(parse_data):
    """Function for creating the final DateFrame for show data in diagramm

    Args:
        parse_data(list) handle data from form

    Return
        DataFrame object with new column 'total_profit' and 'total_revenue',
        and columns by closing price of each stock item

    """

    all_stocks = [get_stock_data(item.stock_id, item.data_start, item.revenue
                                 ) for item in parse_data]
    print('row stocks\n', all_stocks)
    stocks = pandas.DataFrame({item.Close.name: item.Close
                              for item in all_stocks})

    stocks['period'] = ['{}-{}'.format(str(item.year), str(item.month))
                        for item in stocks.index]
    print('all close price with period\n', stocks)
    # get all revenue from stocks and sum this
    agg_revenue = pandas.DataFrame([item.revenue for item in all_stocks])
    stocks['total_revenue'] = agg_revenue.aggregate(np.sum)
    # get all profit from stocks and sum this
    agg_profit = pandas.DataFrame([item.profit for item in all_stocks])
    stocks['total_profit'] = agg_profit.aggregate(np.sum)

    print('all revenue\n', agg_revenue)
    print('all profit\n', agg_profit)
    return stocks.round(2)


def get_stock_data(stock_id, start_date, revenue):
    """Function for obtaining data on each share

    Args:
        stock_id (string) the name of the dataset (by stock)
        start_date (datetime) left boundary for range period
        revenue (float) invested money per stock

    Return:
        DataFrame object with new column 'profit' and 'revenue', and
        aggregated per month

    """
    try:
        start = datetime.datetime.strptime(
            start_date, '%Y-%m-%d'
        ) + datetime.timedelta(days=1)
        data_stock = web.DataReader(stock_id, 'yahoo', start, retry_count=10)
    except RemoteDataError as e:
        data_stock = web.DataReader(stock_id, 'yahoo', start, retry_count=10)
    except (TypeError, ValueError) as e:
        raise RequestError(e)
    stock = data_stock.Close.to_frame()
    stock["profit"] = revenue * ((stock.Close - stock.Close[0]
                                  ) / stock.Close)
    stock["revenue"] = stock.profit + revenue
    stock = stock.groupby(pandas.Grouper(freq='BM')).mean()
    stock.Close.name = stock_id
    # print(stock_id, stock)
    return stock
