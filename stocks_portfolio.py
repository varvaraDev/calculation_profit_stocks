"""Modul for Handling data by stocks portfolio"""
import datetime
from collections import namedtuple

import numpy as np
import pandas
import pandas_datareader.data as web
from pandas_datareader.base import RemoteDataError

from handle_exceptions import RequestError


def parse_form(data):
    """Parsing input values from form.

    Args:
        data (string) data from form by get requsest.
        StockData (namedtuple) class for store data.

    Return:
        parse_item (list) list of objects StockData.

    Raises:
        RequestError: If input data is invalid and raise exceptions
                      when processing.

    """
    parse = [item.split("=") for item in data.split('\r\n')]
    StockData = namedtuple('StockData', 'stock_id, data_start, revenue')
    try:
        parse_item = [StockData(item[0], item[1], float(item[2]))
                      for item in parse]

    except (TypeError, ValueError, IndexError, AttributeError) as e:
        raise RequestError(e)

    return parse_item


def get_stock_data(stock_id, start_date, revenue):
    """Function for obtaining data on each share

    Args:
        stock_id (string) the name of the dataset (by stock).
        start_date (datetime) left boundary for range period.
        revenue (float) invested money per stock.

    Return:
        stock (DataFrame) object with new column 'profit' and 'revenue', and
        aggregated per month.

    Raises:
        RequestError: If input data is invalid and raise exceptions
                      when processing or raise exception RemoteDataError
                      from pandas_datareader.

    """
    try:
        start = datetime.datetime.strptime(
            start_date, '%Y-%m-%d'
        ) + datetime.timedelta(days=1)
        if start > datetime.datetime.today():
            raise ValueError('''Invalid date: start date should
                             be less than today's date!''')

        data_stock = web.DataReader(stock_id, 'yahoo', start, retry_count=8)

    except RemoteDataError as e:
        data_stock = web.DataReader(stock_id, 'yahoo', start, retry_count=8)
    except (TypeError, ValueError) as e:
        raise RequestError(e)

    stock = data_stock.Close.to_frame()
    stock["profit"] = revenue * ((stock.Close - stock.Close[0]
                                  ) / stock.Close)
    stock["revenue"] = stock.profit + revenue
    stock = stock.groupby(pandas.Grouper(freq='BM')).mean()
    stock.Close.name = stock_id
    print(stock_id, stock)

    return stock

# Alternatives aggregated by month
# return stock.resample('BM').mean()
# stock.groupby(pandas.TimeGrouper(freq='BM')).mean()
# (It's deprecated in favor of just pd.Grouper)
#  stocks.resample('M').mean()


def get_final_frame(parse_data):
    """Function create the final DateFrame for show data in diagramm

    Args:
        parse_data(list) handle data from form

    Return
        DataFrame object with new column 'total_profit' and 'total_revenue',
        and columns by closing price of each stock item

    """

    all_stocks = [get_stock_data(item.stock_id, item.data_start, item.revenue
                                 ) for item in parse_data]

    stocks = pandas.DataFrame({item.Close.name: item.Close
                              for item in all_stocks})

    stocks['period'] = ['{}-{}'.format(str(item.year), str(item.month))
                        for item in stocks.index]
    # get all revenue from stocks and sum this
    agg_revenue = pandas.DataFrame([item.revenue for item in all_stocks])
    stocks['total_revenue'] = agg_revenue.aggregate(np.sum)

    # get all profit from stocks and sum this
    agg_profit = pandas.DataFrame([item.profit for item in all_stocks])
    stocks['total_profit'] = agg_profit.aggregate(np.sum)

    return stocks.round(2)
