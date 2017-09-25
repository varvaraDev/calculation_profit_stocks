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
        parse_data = data.split('\r\n')
        parse = [item.split("=") for item in parse_data]
        StockData = namedtuple('StockData', 'stock_id, data_start, revenue')
        parse_item = [StockData(item[0], item[1], item[2]) for item in parse]
        v, p = earnings_stocks(
            parse_item[0].stock_id,
            parse_item[0].data_start,
            parse_item[0].revenue
         )
        date_str = parse_item[0].data_start
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d').year
        name = parse_item[0].stock_id
        data_line = {
            "profit": p.tolist(),
            "revenue": v.tolist(),
            "subtitle": name,
            "date": date
            }

        return render_template(
            'stock.html',
            stock=data_line["subtitle"],
            profit=data_line["profit"],
            revenue=data_line["revenue"],
            date=data_line["date"]
            )


@app.route('/display', methods=['GET', 'POST'])
def display(name='Varvara'):
    if request.method == 'GET':
        title_data = {
            "title": "TOLAL PROFIT"
            }
        return render_template('fail.html', stock=title_data["title"])
        # return "Hello"


if __name__ == "__main__":
    app.run()
