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
    """Function return DataFrame by stock
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

    return data_stock


def handle_stock(data_stock, id_stock, revenue):
    # data_stock["profit"] = revenue / data_stock.Open * (
    #                        data_stock.Close - data_stock.Open)
    # # data_stock["profit"] = data_stock.Open - data_stock.Close
    # data_stock["revenue"] = data_stock.profit + revenue
    data_stock["count_stocks"] = revenue / data_stock.Open[0]
    stock = data_stock.groupby(pandas.Grouper(freq='BM')).mean()
    stock['ID'] = id_stock
    stock['revenue'] = revenue
    # data_stock.Close.name = stock_id
    # print(data_stock)
    return stock.reset_index().set_index(['ID', 'Date'])


def grouper_by_moth(df):
    return df.groupby([df.index.get_level_values(0)]+[pandas.Grouper(
                      freq='BM', level=1)]).mean().round(2)


def main_func(parse):
    list_stock = []
    for item in parse:
        row = get_stock_data(item.stock_id, item.data_start)
        handle = handle_stock(row, item.stock_id, item.revenue)
        list_stock.append(handle)
    result = list_stock[0].append(list_stock[1:])
    # result['profit'] = result.Open - result.Close
    # result['revenue'] = result.revenue + result.profit
    result['profit'] = result.count_stocks * (result.Open - result.Close)
    result['revenue'] = result.count_stocks * result.Close + result.profit
    return grouper_by_moth(result)





def reindex(data_stock, id_stock, revenue):
    data_stock["count_stocks"] = round(revenue / data_stock.Open, 4)
    data_stock = data_stock.reset_index().set_index('Date', 'ID')
    data_stock = data_stock.groupby(pandas.Grouper(freq='BM')).mean()
    return data_stock





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




# Для получения периода (индеком становится дата)
# f.profit.unstack(level=1)

# Для получения среза по ID
# f.xs('GOOG', level='ID')
# Для получения total_profit
 # f.profit.unstack(level=1).sum(axis=1, skipna=True)

# groupby by date
# f.profit.reset_index()
# Alternatives aggregated by month
# return stock.resample('BM').mean()
# stock.groupby(pandas.TimeGrouper(freq='BM')).mean()
# (It's deprecated in favor of just pd.Grouper)
#  stocks.resample('M').mean()

# ['{}-{}'.format(str(item.year), str(item.month)) for item in result.reset_index().Date.tolist()]

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
