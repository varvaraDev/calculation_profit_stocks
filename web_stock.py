"""Starting module for web application."""

from flask import Flask, render_template, request

from handle_exceptions import RequestError, RemoteDataError_mess
from pandas_datareader.base import RemoteDataError
from stocks_portfolio import get_final_frame, parse_form

app = Flask(__name__)


@app.route('/stocks', methods=['GET', 'POST'])
def stocks():
    """Maim function for calculate profil of stocks.

    Args:
        parse_form (string) parse data from form
        id_stocks (string) id by stocks
        result (DateFrame) table with handle stocks
        stock_close (list) closing price of each stock item

    Return:
        if method 'GET' - html page with form.
        if method 'POST' - html page with diagramm of calculate portfolio.
        if raise exceptions - html page witn message about error.

    """
    if request.method == 'GET':
        return render_template('form.html')

    if request.method == 'POST':
        parse = parse_form(request.form["textcontent"])
        print(parse)
        id_stocks = [item.stock_id for item in parse]
        result = get_final_frame(parse)

        stock_close = [
            (
                id_stock,
                result[id_stock].tolist()
            ) for id_stock in id_stocks]

        print('DataFrame with all data\n', result)
        print('For serias\n', stock_close)

    return render_template(
            'stock.html',
            profit=result.total_profit.tolist(),
            revenue=result.total_revenue.tolist(),
            stock_close=stock_close,
            period=result.period.tolist(),
            data_form=request.form["textcontent"].split('\r\n')
            )


@app.errorhandler(RequestError)
def handle_invalid_usage(error):
    """Exception Handler for app"""
    mess = error.get_data()
    return render_template(
           'error.html',
           message=mess
        )


@app.errorhandler(RemoteDataError)
def handle_remote_data_error(error):
    """Exception Handler for app"""
    mess = RemoteDataError_mess.replace('\n', '')
    return render_template(
           'error.html',
           message=mess
        )


if __name__ == "__main__":
    app.run(debug=True)
