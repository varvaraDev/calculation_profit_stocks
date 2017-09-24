import datetime
from collections import namedtuple

import pandas_datareader.data as web
from pandas_datareader.base import RemoteDataError

from calculate import profit_collum, revenue_collum


class RequestError(Exception):
    """Raises if the arguments of the sex method are not spouses
    """

def get_stock(stock_id, start_date):
    end = datetime.date.today()
    try:
        start = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        stock = web.DataReader(stock_id, 'yahoo', start, end)
    except RemoteDataError as e:
        stock = web.DataReader(stock_id, 'yahoo', start, end)
    except (TypeError, ValueError) as e:
        return(data)
    return stock.Close

def earnings_stocks(stock_id, start_date, revenue):
    # end_date = format(datetime.date.today(), '%Y-%m-%d')
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
    # close = stock.loc[:, "Close"]
    close = stock.Close
    old_cost = float(close[0])
    print(type(old_cost))
    profit = close.apply(profit_collum, args=(old_cost, revenue))
    new_revenue = profit.apply(revenue_collum, args=(revenue,))
    month_revenue = new_revenue.resample('M').mean()
    month_profit = profit.resample('M').mean()
    # print(month_revenue, month_profit)
    return month_revenue, month_profit
    # return month_revenue.tolist(), month_profit.tolist()
# month = stock.groupby(pandas.Grouper(freq='M')).sum()
# month = stock.groupby(pandas.TimeGrouper(freq='M')).agg(numpy.sum)

def earnings_stocks_test(stock_id, start_date, revenue):
    # end_date = format(datetime.date.today(), '%Y-%m-%d')
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
    # print(month_revenue, month_profit)
    return stock

def total_earnings_profit(*args):
    return sum(list(args))


# appl = earnings_stocks_test('AAPL', '2016-12-24', 1200.0)
# googl = earnings_stocks_test('GOOG', '2001-01-01', 500.0)
# amzn = earnings_stocks_test('AMZN', '2012-01-01', 150.0)
# stocks_all = pd.DataFrame({"AAPL": stock1["Close"], "MSFT": stock2["Close"],"GOOG": stock3["Close"]})
# old_cost2 = stock2.Close[0]                                                                      │
# profit2 = exp.MSFT.apply(profit_collum, args=(old_cost, 150))
def total_earnings_revenue(*args):
    return sum(list(args))

# data = 'AAPL=2016-12-24=1200\r\nGOOG=2001-01-01=50\r\nAMZN=2012-01-01=150'
# d1= data.split('\r\n')
# parse = [item.split("=") for item in d1]
# data2 = [{"id": item[0], "data_start": item[1], "rev": item[2]} for item in parse]
# from collections import namedtuple
# StockData = namedtuple('StockData', 'stock_id, data_start, revenue')
# p = StockData('AAPL=2016-12-24=1200'.split("="))
# data2 = [StockData(item[0], item[1], item[2]) for item in parse]
# p, v = earnings_stocks(data2[0].stock_id, data2[0].data_start, data2[0].revenue)


# new_revenue = prof.apply(revenue_collum, args=(1200,))
# Get data about projects
# so we do cumsum over period of time so we can see the growth
# gp = df.groupby(['period', 'project']).agg({'minutes':'sum'})
# gp = gp.unstack(level=1)
# gp.groupby(pd.TimeGrouper(freq='M')).sum().cumsum().plot.area(alpha=0.75, linewidth=4., figsize=(20, 10))
# # over quarters
# gp.groupby(pd.TimeGrouper(freq='Q')).sum().cumsum().plot.area(alpha=0.75, linewidth=4., figsize=(20, 10))
# # over weeks
# gp.groupby(pd.TimeGrouper(freq='W')).sum().cumsum().plot.area(alpha=0.75, linewidth=4., figsize=(20, 10))


def get_profit_all(handle_stocks):
    """Join all DataFrame by stocks and fitering by month"""
    merge_stock = []
    StockMonth = namedtuple('StockMonth',
                            'stock_id, revenue, profit')
    dict_profut = {item.stock_id: item.profit for item in handle_stocks}
    profit_merge = pandas.DataFrame(dict_profut)
    dict_revenue = {item.stock_id: item.revenue for item in handle_stocks}
    revenue_merge = pandas.DataFrame(dict_revenue)
    profit_merge = profit_merge.fillna(0)
    revenue_merge = revenue_merge.fillna(0)
    month_profit = profit_merge.resample('M').mean()
    month_revenue = revenue_merge.resample('M').mean()
    for item in handle_stocks:
        stock = StockMonth(
            stock_id=item.stock_id,
            profit=month_profit[item.stock_id],
            revenue=month_revenue[item.stock_id]
         )
        merge_stock.append(stock)
    return merge_stock

def calculate_profit_revenue(row_stocks):
    """First parse of stocks. Returns an object DataFrame for each stock """
    StockCallculate = namedtuple('StockCallculate',
                                 'stock_id, revenue, profit')
    handle_stocks = []
    for item in row_stocks:
        profit = item.stock.apply(
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


def get_dataframe(all_list):
    """Join all DataFrame by stocks and fitering by month"""
    fdict = {item.stock_id: item.stock for item in all_list}
    stocks_all = pandas.DataFrame(fdict)
    stocks_all = stocks_all.fillna(0)
    month = stocks_all.resample('M').mean()
    return month


def new_stocks(all_list, stocks_all):
    """Processing a Data Set. Calculate profit, revenue for each stock

    Returns a list of objects with attributes
    """
    Stocks = namedtuple('Stocks', 'stock_id, profit, revenue')
    new_list = []
    for item in all_list:
        profit = stocks_all[item.stock_id].apply(
            profit_collum,
            args=(item.first_cost, item.revenue)
         )
        diff_revenue = profit.apply(revenue_collum, args=(item.revenue,))
        new_stock = Stocks(
            stock_id=item.stock_id,
            profit=profit,
            revenue=diff_revenue
            )
        new_list.append(new_stock)
    return new_list


def list_stocks(parse_item):
    """First list stock """
    stock_list = []
    for item in parse_item:
        stock = get_stock(
            item.stock_id,
            item.data_start
         )
        stock_list.append(stock)
    return stock_list

    form = request.form["textcontent"]
    parse_form = parse_str(form)
    row = row_stocks(parse_form)
    handle_stock = calculate_profit_revenue(row)
    result = get_data_all(handle_stock)
    period = ['{}-{}'.format(str(item.year),
              str(item.month)) for item in result[0].revenue.index]
    # total_profit = sum([item.profit for item in result])
    # total_revenue = sum([item.revenue for item in result])
    total_profit = calculate_total(result, True)
    total_revenue = calculate_total(result, False)
    # period = ['{}-{}'.format(str(item.year),
    #           str(item.month)) for item in total_revenue.index]

@app.route('/display', methods=['GET', 'POST'])
def display(name='Varvara'):
    if request.method == 'GET':
        title_data = {
            "title": "TOLAL PROFIT",
            "cat":  ['2016-12',
                     '2017-1',
                     '2017-2',
                     '2017-3',
                     '2017-4',
                     '2017-5',
                     '2017-6',
                     '2017-7',
                     '2017-8',
                     '2017-9'],
            "stock": "GOOG",
            "profit": [0.9891805601149203,
                       30.354634041536485,
                       153.78925029878783,
                       205.50406011081373,
                       221.36660407586686,
                       281.13702062510134,
                       253.3704653538376,
                       256.7156508822362,
                       320.39978176099555,
                       333.9419327824898],
            "revenue": [1200.989180560115,
                        1230.3546340415364,
                        -1353.7892502987881,
                        1405.5040601108137,
                        1421.3666040758667,
                        1481.137020625101,
                        1453.3704653538377,
                        1456.715650882236,
                        1520.399781760996,
                        1532.5443756875277]

            }
        create_diagramm_test(title_data["profit"], title_data["revenue"], title_data["cat"])
    return render_template(
        'test.html'
        )


def create_diagramm_test(total_profit, total_revenue, period):
    """Function created diagramm from the calculated values

    Return html file
    """
    H = Highchart()
    H.set_options('title', {'text': "GOOG"})
    H.add_data_set(total_profit, 'line', 'TOTAL PROFIT')
    H.add_data_set(total_revenue, 'line', 'TOTAL REVENUE')
    H.set_options('yAxis', {'title': {'text': 'USD'},
                  'plotLines': {'value': -250, 'width': 1, 'color': '#808080'},
                  'tickInterval': 250, 'gridLineWidth': 2})
    # H.set_options('yAxis', {'title': {'text': 'USD'}, 'tickInterval': 250, 'gridLineWidth': 2})
    H.set_options('xAxis', {'categories': period, 'type': 'datetime', 'gridLineWidth': 1})
    H.set_options('legend', {'layout': 'horizontal',
                             'align': 'center',
                             'verticalAlign': 'bottom',
                             'borderWidth': 0})
    H.save_file("templates/test")


# class RequestError(Exception):
#     '''raise if input data not correct'''
#     def __init__(self, errore):
#         Exception.__init__(self)
#         self.errore = errore
#         self.true = data_correct

# step 1
