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


def get_stock_data(stock_id, start_date):
    """Function return DataFrame by stock.

    Args:
        stock_id (string) the name of the dataset (by stock).
        start_date (datetime) left boundary for range period.
        revenue (float) invested money per stock.

    Return:
        stock (DataFrame) object with data by stock

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

    return data_stock


def handle_stock(data_stock, id_stock, revenue):
    """Function add MultiIndex and column in DataFrame

    Args:
        data_stock (DateFrame) object by stock
        id_stock (string) ID stock
        revenue (float) investments in the purchase

    Return:
        DataFrame with two index - ID and Date, new column 'count stock'"""
    # data_stock["profit"] = revenue / data_stock.OpenFock.Open)
    # # data_stock["profit"] = data_stock.Open - data_stock.Close
    # data_stock["revenue"] = data_stock.profit + revenue
    # data_stock["count_stocks"] = revenue / data_stock.Opens
    # stock = data_stock.groupby(pandas.Grouper(freq='BM')).mean()
    data_stock['ID'] = id_stock
    return data_stock.reset_index().set_index(['ID', 'Date'])


def grouper_by_moth(df):
    """Return DataFrame aggregated by month and round."""
    return df.groupby([df.index.get_level_values(0)]+[pandas.Grouper(
                      freq='BM', level=1)]).mean().round(2)






def revenue_all(s, parse):
    revenue = []
    for item in parse:
        revenue.append(s.loc[slice(item.stock_id, item.stock_id), :] + item.revenue)
    return revenue[0].append(revenue[1:])

def revenue_true(s, parse, Open, count):
    revenue = []
    for item in parse:
        revenue.append(s.loc[slice(item.stock_id, item.stock_id), :] +
                       Open.xs(item.stock_id) * count.xs(item.stock_id))
    return revenue[0].append(revenue[1:])


def count_stock(s, parse):
    count = []
    for item in parse:
        count.append(
            item.revenue / s.loc[slice(item.stock_id, item.stock_id), :]
            )
    return count[0].append(count[1:])


def aggregated_data_stocks(parse):
    """Main function for create a final DataFrame"""
    list_stock = []
    for item in parse:
        row = get_stock_data(item.stock_id, item.data_start)
        handle = handle_stock(row, item.stock_id, item.revenue)
        list_stock.append(handle)
    result = list_stock[0].append(list_stock[1:])
    # result['profit'] = result.Open - result.Close
    # result['revenue'] = result.revenue + result.profit
    result.sort_index(inplace=True)
    result['count_stocks'] = result.Close.to_frame().apply(
        count_stock, args=(parse,)
     )
    result['profit'] = result.count_stocks * (result.Open - result.Close)
    result['revenue'] = result.profit.to_frame().apply(
        revenue_true,
        args=(parse, result.Open, result.count_stocks)
     )
    return grouper_by_moth(result)

# def calculate_profit(result, parse):
#     stock_data = aggregated_data_stocks(parse)

def aggregated(parse):
    """Return aggregated DataFrame"""
    list_stock = []
    for item in parse:
        row = get_stock_data(item.stock_id, item.data_start)
        handle = handle_stock(row, item.stock_id, item.revenue)
        list_stock.append(handle)
    result = list_stock[0].append(list_stock[1:])
    return result

def count_revenue_simpl(s, parse):
    """Add sum revenue."""
    revenue = []
    for item in parse:
            revenue.append(s.loc[slice(item.stock_id, item.stock_id), :] + item.revenue)
    return revenue[0].append(revenue[1:])




# result['profit'] = result.count_stocks * (result.Close - result.Open)
#
# result['profit'] = result.Close - result.Open
# #
# result['profit'] = result.count_stocks * result.Open + (result.Close - result.Open)
# row_stock = []
# for item in parse:
#     s1 = get_stock_data(item.stock_id, item.data_start, item.revenue)
#     row_stock.append(s1)
#
# total = [row_stock[0].append(item) for item in row_stock]
#
# add_collum = []



# def add_profit_revenue(data_stock, revenue):
#     # data_stock["profit"] = revenue / data_stock.Open * (
#     #                        data_stock.Close - data_stock.Open)
#     # # data_stock["profit"] = data_stock.Open - data_stock.Close
#     # data_stock["revenue"] = data_stock.profit + revenue
#     data_stock['ID'] = id_stock
#     data_stock["count_stocks"] = round(revenue / data_stock.Open, 4)
#     data_stock = data_stock.groupby(pandas.Grouper(freq='BM')).mean()
#     # data_stock.Close.name = stock_id
#     # print(data_stock)
#     return data_stock






# ['{}-{}'.format(str(item.year), str(item.month)) for item in result.reset_index().Date.tolist()]
