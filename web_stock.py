from flask import Flask, request, render_template
from flask import json
from collections import namedtuple
import pandas
from stocks_portfolio import earnings_stocks
import datetime
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
        date = [str(item.year) + '-' + str(item.month) for item in v.index]
        data_line = {
            "profit": p.tolist(),
            "revenue": v.tolist(),
            "title": name,
            "date": date
            }

        return render_template(
            'stock.html',
            stock=data_line["title"],
            profit=data_line["profit"],
            revenue=data_line["revenue"],
            date=data_line["date"]
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
        return render_template(
            'stock.html',
            stock=title_data["title"],
            profit=title_data["profit"],
            revenue=title_data["revenue"],
            date=title_data["cat"]
            )


def parse_str(data):
    parse_data = data.split('\r\n')
    parse = [item.split("=") for item in parse_data]
    StockData = namedtuple('StockData', 'stock_id, data_start, revenue')
    parse_item = [StockData(item[0], item[1], item[2]) for item in parse]
    return parse_item


if __name__ == "__main__":
    app.run()
