"""Starting module for web application."""

from flask import Flask, render_template, request
# from highcharts import Highchart

from stocks_portfolio import (
    parse_str,
    all_stocks_ver1
    )

app = Flask(__name__)


@app.route('/stocks', methods=['GET', 'POST'])
def stocks():
    """Maim function for calculate profil of stocks.
    Args:
        response (html) response for get request,
        by get data of stocks with form.
        form (string) Data of forms textarea
        row (string) resul parse of data
        handle_stock (list) List of frame objects by stocks
        result (list) treated data on shares
        total_profit, total_revenue (obj) - result profit and revenue of
        all_data
    """
    if request.method == 'GET':
        response = """
            <html>
            <head>
            <meta charset="utf-8">
            <title>Handling stocks</title>
            </head>
            <body>
            <form action='/stocks' method="post">
                <p><b>Input you portfolio:</b></p>
                <p>
                <textarea name="textcontent" rows="10" cols="45"></textarea>
                </p>
                <p><input type="submit" value="Send"></p>
            </form>
                </body>
            </html>
        """
        return response

    if request.method == 'POST':
        parse_form = parse_str(request.form["textcontent"])
        result = all_stocks_ver1(parse_form)
        id_stocks = [item.stock_id for item in parse_form]
        stock_close = [result[id_stock] for id_stock in id_stocks]

    return render_template(
            'stock.html',
            profit=result.total_profit.tolist(),
            revenue=result.total_revenue.tolist(),
            stock_close=stock_close,
            period=result.period
            )


@app.route('/display', methods=['GET', 'POST'])
def display():
    if request.method == 'GET':
            total_revenue = [1505.46, 1501.24, 1511.61, 1507.71, 1500.74, 1483.47, 1496.1, 1529.12, 1556.83, 1560.68]
            total_profit = [-102.25, -117.09, -73.87, -90.03, -119.39, -199.55, -141.19, -6.17, 87.04, 97.41]
            period = ['2012-1',
                         '2012-2',
                         '2012-3',
                         '2012-4',
                         '2012-5',
                         '2012-6',
                         '2012-7',
                         '2012-8',
                         '2012-9',
                         '2012-10']
            nan = None
            # close_stock = [[200, 100, 120, 111, 133, 555, 666, 444, 333, 555],
            #  [305.4577928,
            #   301.23897845,
            #   311.60941518181824,
            #   307.7141159000001,
            #   300.73807877272725,
            #   283.46869195238094,
            #   296.09916033333343,
            #   329.1165892173913,
            #   356.8302132105262,
            #   360.682203047619],
            #  [444, 111, 333, 444, 555, 333, 1223, 103, 434, 100]]
            close_stock = [[nan, nan, nan, nan, nan, nan, 103, 434, 100, 100],
             [305.4577928,
              301.23897845,
              311.60941518181824,
              307.7141159000001,
              300.73807877272725,
              283.46869195238094,
              296.09916033333343,
              329.1165892173913,
              356.8302132105262,
              360.682203047619],
             [nan, nan, nan, nan, nan, 555, 333, 1223, 103, 434, 100]]
            # close_stock = [('AAPL', [nan, nan, nan, nan, nan, nan, nan, nan, nan, nan]),
            #                  ('GOOG',
            #                   [305.4577928,
            #                    301.23897845,
            #                    311.60941518181824,
            #                    307.7141159000001,
            #                    300.73807877272725,
            #                    283.46869195238094,
            #                    296.09916033333343,
            #                    329.1165892173913,
            #                    356.8302132105262,
            #                    360.682203047619]),
            #                  ('AMZN', [nan, nan, nan, nan, nan, nan, nan, nan, nan, nan])]
    stocks_id = ['AAPL', 'GOOG', 'AMZN']
    return render_template(
            'stock.html',
            profit=total_profit,
            revenue=total_revenue,
            stock_close=close_stock,
            period=period,
            stocks_id=stocks_id
            )


if __name__ == "__main__":
    app.run()
