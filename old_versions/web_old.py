"""Starting module for web application."""

from flask import Flask, render_template, request
from highcharts import Highchart

from stocks_portfolio import (
    parse_str,
    row_stocks,
    calculate_profit_revenue,
    get_data_all,
    calculate_total
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

        form = request.form["textcontent"]
        parse_form = parse_str(form)
        row = row_stocks(parse_form)
        handle_stock = calculate_profit_revenue(row)
        result = get_data_all(handle_stock)
        period = ['{}-{}'.format(str(item.year),
                  str(item.month)) for item in result[0].revenue.index]
        total_profit = calculate_total(result, True)
        total_revenue = calculate_total(result, False)
        create_diagramm(
            portfolio=result,
            total_profit=total_profit,
            total_revenue=total_revenue,
            period=period
            )

        return render_template(
            'stock_hero.html'
            )


def create_diagramm(portfolio, total_profit, total_revenue, period):
    """Function created diagramm from the calculated values.
    Args:
        portfolio (list) - all handle stocks
        total_profit (list)- aggregated profit by all stocks
        total_revenue (list)- aggregated revenue by all stocks
        period - Time season from the date of the first purchase of shares
    Return:
        html file with crated diagramm
    """
    H = Highchart()
    H.set_options('title', {'text': "Calculate profil of stocks"})
    for item in portfolio:
        H.add_data_set(item.profit.tolist(), 'line', 'Profit {}'.format(
            item.stock_id)
            )
        H.add_data_set(item.revenue.tolist(), 'line', 'Revenue {}'.format(
            item.stock_id)
            )
    H.add_data_set(total_profit, 'line', 'TOTAL PROFIT')
    H.add_data_set(total_revenue, 'line', 'TOTAL REVENUE')
    H.set_options('yAxis', {'title': {'text': 'USD'},
                  'plotLines': {'value': -250, 'width': 1, 'color': '#808080'},
                            'tickInterval': 250, 'gridLineWidth': 2,
                            'min': -500})
    H.set_options('xAxis', {'categories': period, 'type': 'datetime'})
    H.set_options('legend', {'layout': 'horizontal',
                             'align': 'center',
                             'verticalAlign': 'bottom',
                             'borderWidth': 0})
    H.save_file("templates/stock_hero")

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
            # close_stock = [[nan, nan, nan, nan, nan, nan, 103, 434, 100, 100],
            #  [305.45,
            #   301.23,
            #   311.60,
            #   307.71,
            #   300.73,
            #   283.46,
            #   296.09,
            #   329.11,
            #   356.83,
            #   360.68],
            #  [nan, nan, nan, nan, nan, 555, 333, 122, 103, 434]]
            close_stock = [('AAPL', [nan, nan, nan, nan, nan, nan, 103, 434, 100, 100]),
                             ('GOOG',
                              [305.4577928,
                               301.23897845,
                               311.60941518181824,
                               307.7141159000001,
                               300.73807877272725,
                               283.46869195238094,
                               296.09916033333343,
                               329.1165892173913,
                               356.8302132105262,
                               360.682203047619]),
                             ('AMZN', [nan, nan, nan, nan, nan, 555, 333, 1223, 103, 434])]
            # close_stock = [['AAPL', [nan, nan, nan, nan, nan, nan, 103, 434, 100, 100]],
            #                  ['GOOG',
            #                   [305.4577928,
            #                    301.23897845,
            #                    311.60941518181824,
            #                    307.7141159000001,
            #                    300.73807877272725,
            #                    283.46869195238094,
            #                    296.09916033333343,
            #                    329.1165892173913,
            #                    356.8302132105262,
            #                    360.682203047619]],
            #                  ['AMZN', [nan, nan, nan, nan, nan, 555, 333, 1223, 103, 434, 100]]]
    stocks_id = ['AAPL', 'GOOG', 'AMZN']
    portfolio = 'AAPL=2016-12-24=1200\r\nGOOG=2012-01-01=500\r\nAMZN=2012-01-01=800'.split('\r\n')
    return render_template(
            'stock.html',
            profit=total_profit,
            revenue=total_revenue,
            stock_close=close_stock,
            period=period,
            stocks_id=stocks_id,
            data_form=portfolio
            )


if __name__ == "__main__":
    app.run()
