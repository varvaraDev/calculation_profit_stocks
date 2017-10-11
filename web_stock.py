"""Starting module for web application."""

from flask import Flask, render_template, request
from pandas_datareader.base import RemoteDataError

from handle_exceptions import RemoteDataError_mess, RequestError
from stocks_portfolio import main_func, parse_form

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
        result = main_func(parse)
        print(parse)
        print(result)
    return render_template(
            'stock.html',
            result=result,
            data_form=request.form["textcontent"].split('\r\n')
            )


@app.errorhandler(RequestError)
def handle_invalid_usage(error):
    """Exception Handler exception RequestError for app."""
    mess = error.get_data()
    return render_template(
           'error.html',
           message=mess
        )


@app.errorhandler(RemoteDataError)
def handle_remote_data_error(error):
    """Exception Handler if invalid id by stocks."""
    mess = RemoteDataError_mess.replace('\n', '')
    return render_template(
           'error.html',
           message=mess
        )


if __name__ == "__main__":
    app.run(debug=True)
