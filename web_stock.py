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


if __name__ == "__main__":
    app.run()
