"""Modul for Handling data by stocks portfolio."""
import datetime
from collections import namedtuple

import pandas_datareader.data as web
from pandas_datareader.base import RemoteDataError

from calculate import (count_revenue_apply, count_revenue_func,
                       count_stock_func, grouper_by_moth)
from handle_exceptions import RequestError


def main_func(parse):
    """Return final DataFrame for diagramm.

    Args:
        parse (list) parsind data from form

    Return:
        Aggregated DataFrame with all data

    """
    result = aggregated_stocks(parse)
    result['profit_one'] = result.Open - result.Close
    result['profit'] = result.count_stocks * (result.Open - result.Close)
    result['revenue'] = result.profit.to_frame().apply(
        count_revenue_apply,
        args=(parse,)
     )
    return grouper_by_moth(result)


def aggregated_stocks(parse):
    """Function for aggregated DataFrame

    Args:
        parse (list) data of stocks

    Return
        DataFrame object witn MultiIndex

    """
    list_stock = []
    for item in parse:
        row = get_stock_data(item.stock_id, item.data_start)
        handle = handle_stock(row, item.stock_id, item.revenue)
        list_stock.append(handle)
    if len(list_stock) == 1:
        list_stock[0].sort_index(inplace=True)
        return list_stock[0]
    result = list_stock[0].append(list_stock[1:])
    result.sort_index(inplace=True)
    return result


def get_stock_data(stock_id, start_date):
    """Function return DataFrame by stock.

    Args:
        stock_id (string) the name of the dataset (by stock).
        start_date (datetime) left boundary for range period.

    Return:
        stock (DataFrame) object with data by stock

    Note: Use method fillna (replace None on zero), becouse delete empty values.
          See stock BTCUSD=X 2016-01-01 5000 (not data 2016 02-11)

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

    return data_stock.fillna(0)


def handle_stock(data_stock, id_stock, revenue):
    """Function add MultiIndex and columns in DataFrame.

    Args:
        data_stock (DateFrame) object by stock
        id_stock (string) ID stock
        revenue (float) investments in the purchase

    Return:
        DataFrame with two index - ID and Date, new column 'count stock'
    """
    data_stock["count_stocks"] = revenue / data_stock.Open[0]
    data_stock['ID'] = id_stock
    return data_stock.reset_index().set_index(['ID', 'Date'])


def parse_form(data):
    """Parsing input values from form.s

    Args:
        data (string) data from form by get requsest.
        StockData (namedtuple) class for store data.

    Return:
        parse_item (list) list of objects StockData.

    Raises:
        RequestError: If input data is invalid and raise exceptions
                      when processing.

    """
    parse = [item.split(" ") for item in data.split('\r\n')]
    StockData = namedtuple('StockData', 'stock_id, data_start, revenue')
    try:
        parse_item = [StockData(item[0], item[1], float(item[2]))
                      for item in parse]

    except (TypeError, ValueError, IndexError, AttributeError) as e:
        raise RequestError(e)
    return parse_item
