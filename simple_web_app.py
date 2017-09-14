from flask import Flask, request, render_template
from flask import json
from collections import namedtuple
import pandas
from simple_stocks import earnings_stocks
import datetime
from highcharts import Highchart
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
        v, p = earnings_stocks(
            parse_item[0].stock_id,
            parse_item[0].data_start,
            parse_item[0].revenue
         )
        date_str = parse_item[0].data_start
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d').year
        name = parse_item[0].stock_id
        date = ['{}-{}'.format(str(item.year),
                str(item.month)) for item in v.index]
        # print(date, len(date))
        # print(v, len(v))
        # print(p, len(p))
        # data_line = {
        #     "profit": p.tolist(),
        #     "revenue": v.tolist(),
        #     "title": name,
        #     "date": date
        #     }

        create_diagramm(
            profit=p.tolist(),
            revenue=v.tolist(),
            stock_id=name,
            period=date)

        return render_template(
            'result.html')

        # return render_template(
        #     'stock_simple.html',
        #     stock=data_line["title"],
        #     profit=data_line["profit"],
        #     revenue=data_line["revenue"],
        #     date=data_line["date"]
        #     )

def parse_str(data):
    parse_data = data.split('\r\n')
    parse = [item.split("=") for item in parse_data]
    StockData = namedtuple('StockData', 'stock_id, data_start, revenue')
    parse_item = [StockData(item[0], item[1], item[2]) for item in parse]
    return parse_item

def create_diagramm(profit, revenue, stock_id, period):
    H = Highchart()
    H.set_options('title', {'text': "Calculate profil of stocks"})
    H.add_data_set(profit, 'line', 'Profit {}'.format(stock_id))
    H.add_data_set(revenue, 'line', 'Revenue {}'.format(stock_id))
    H.set_options('yAxis', {'title': {'text': 'USD'},
                  'plotLines': {'value': 0, 'width': 1, 'color': '#808080'}})
    H.set_options('xAxis', {'categories': period})
    H.set_options('legend', {'layout': 'vertical',
                             'align': 'right',
                             'verticalAlign': 'middle',
                             'borderWidth': 0})
    H.save_file("templates/result")
    for item in all_data:
        H.add_data_set(item.profit.tolist(), 'line', 'Profit {}'.format(item.stock_id))
        H.add_data_set(item.revenue.tolist(), 'line', 'Revenue {}'.format(item.stock_id))
    maximum_period = max([item.date for item in all_data], key=len)

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
        # return render_template(
        #     'stock.html',
        #     stock=title_data["title"],
        #     profit=title_data["profit"],
        #     revenue=title_data["revenue"],
        #     date=title_data["cat"]
        #     )
        return render_template('result_test.html')



if __name__ == "__main__":
    app.run()
