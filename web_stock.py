from flask import Flask, request, render_template
from flask import json
from collections import namedtuple
import pandas
from stocks_portfolio import earnings_stocks
import datetime
from highcharts import Highchart
import pandas_datareader.data as web
from pandas_datareader.base import RemoteDataError
from calculate import profit_collum, revenue_collum
app = Flask(__name__)


@app.route('/stocks', methods=['GET', 'POST'])
def stocks():
    if request.method == 'GET':
        response = """
            <html>
            <head>
            <meta charset="utf-8">
            <title>Handling stocks</title>
            </head>
            <body>
            <form action='/stocks' method="post">
                <textarea name="textcontent" cols="40" rows="4"></textarea>
                <input type="submit">
            </form>
                </body>
            </html>
        """
        return response

    if request.method == 'POST':

        data = request.form["textcontent"]
        parse_item = parse_str(data)
        first_list = get_frames(parse_item)
        dataframe = get_dataframe(first_list)
        all_data = new_stocks(first_list, dataframe)
        total_profit = sum([item.profit for item in all_data])
        total_revenue = sum([item.revenue for item in all_data])
        period = ['{}-{}'.format(str(item.year),
                  str(item.month)) for item in total_revenue.index]
        create_diagramm(
            all_data,
            total_profit.tolist(),
            total_revenue.tolist(),
            period
            )

        return render_template(
            'stock_hero.html'
            )


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
                        1353.7892502987881,
                        1405.5040601108137,
                        1421.3666040758667,
                        1481.137020625101,
                        1453.3704653538377,
                        1456.715650882236,
                        1520.399781760996,
                        1532.5443756875277]

            }
        return render_template('my_line.html')


def get_stock(stock_id, start_date):
    end = datetime.date.today()
    try:
        start = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        stock = web.DataReader(stock_id, 'yahoo', start, end)
    except RemoteDataError as e:
        stock = web.DataReader(stock_id, 'yahoo', start, end)
    return stock.Close


def get_frames(parse_item):
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
            first_cost=float(stock[0]))
        all_list.append(frame)
    return all_list


def get_dataframe(all_list):
    fdict = {item.stock_id: item.stock for item in all_list}
    stocks_all = pandas.DataFrame(fdict)
    stocks_all = stocks_all.fillna(0)
    month = stocks_all.resample('M').mean()
    return month


def new_stocks(all_list, stocks_all):
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


def parse_str(data):
    parse_data = data.split('\r\n')
    parse = [item.split("=") for item in parse_data]
    StockData = namedtuple('StockData', 'stock_id, data_start, revenue')
    parse_item = [StockData(item[0], item[1], float(item[2]))
                  for item in parse]
    return parse_item


def create_diagramm(all_list, profit, revenue, period):
    H = Highchart()
    H.set_options('title', {'text': "Calculate profil of stocks"})
    for item in all_list:
        H.add_data_set(item.profit.tolist(), 'line', 'Profit {}'.format(
            item.stock_id)
            )
        H.add_data_set(item.revenue.tolist(), 'line', 'Revenue {}'.format(
            item.stock_id)
            )
    H.add_data_set(profit, 'line', 'TOTAL PROFIT')
    H.add_data_set(revenue, 'line', 'TOTAL REVENUE')
    H.set_options('yAxis', {'title': {'text': 'USD'},
                  'plotLines': {'value': 0, 'width': 1, 'color': '#808080'}})
    H.set_options('xAxis', {'categories': period})
    # H.set_options('legend', {'layout': 'vertical',
    #                          'align': 'right',
    #                          'verticalAlign': 'middle',
    #                          'borderWidth': 0})
    H.save_file("templates/stock_hero")


if __name__ == "__main__":
    app.run()
