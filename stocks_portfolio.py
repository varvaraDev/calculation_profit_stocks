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
        return parse_item
    except (TypeError, ValueError, IndexError) as e:
        raise e
# step 2

# step 2


def row_stocks(parse_item):
    """First parse of stocks. Returns an object DataFrame for each stock """
    StockAllData = namedtuple('StockAllData',
                              'stock_id, revenue, stock, first_cost')
    all_list = []
    for item in parse_item:
        stock = get_stock(
            item.stock_id,
            item.data_start
         )
        frame = StockAllData(
            stock_id=item.stock_id,
            revenue=float(item.revenue),
            stock=stock,
            first_cost=round(float(stock[0]), 2)
            )
        all_list.append(frame)
    return all_list


def calculate_profit_revenue(row_stocks):
    """First parse of stocks. Returns an object DataFrame for each stock """
    StockCallculate = namedtuple('StockCallculate',
                                 'stock_id, revenue, profit')
    handle_stocks = []
    for item in row_stocks:
        stock = item.stock.resample('M').mean()
        profit = stock.apply(
            profit_collum,
            args=(item.first_cost, item.revenue, )
         )
        diff_revenue = profit.apply(
            revenue_collum,
            args=(item.revenue,)
         )
        frame = StockCallculate(
            stock_id=item.stock_id,
            profit=profit,
            revenue=diff_revenue
            )
        handle_stocks.append(frame)
    return handle_stocks


def get_data_all(handle_stocks):
    """Join all DataFrame by stocks and fitering by month"""
    merge_stock = []
    StockMonth = namedtuple('StockMonth',
                            'stock_id, revenue, profit')
    dict_profut = {item.stock_id: item.profit for item in handle_stocks}
    profit_merge = pandas.DataFrame(dict_profut)
    dict_revenue = {item.stock_id: item.revenue for item in handle_stocks}
    revenue_merge = pandas.DataFrame(dict_revenue)
    # profit_merge = profit_merge.fillna(0)
    # revenue_merge = revenue_merge.fillna(0)
    for item in handle_stocks:
        stock = StockMonth(
            stock_id=item.stock_id,
            profit=profit_merge[item.stock_id],
            revenue=revenue_merge[item.stock_id]
         )
        merge_stock.append(stock)
    return merge_stock


def calculate_total(all_data, sort_profit):
    if sort_profit:
        total = sum([item.profit for item in all_data])
    if not sort_profit:
        total = sum([item.revenue for item in all_data])
    total_round = [round(item, 2) for item in total]
    return total_round


def get_stock(stock_id, start_date):
    end = datetime.date.today()
    try:
        start = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        stock = web.DataReader(stock_id, 'yahoo', start, end)
    except RemoteDataError as e:
        stock = web.DataReader(stock_id, 'yahoo', start, end)
    except (TypeError, ValueError) as e:
        raise e
    return stock.Close
