import datetime
import pandas_datareader.data as web
from pandas_datareader.base import RemoteDataError
from calculate import profit_collum, revenue_collum


# test1 = web.DataReader('GOOG', 'yahoo', start_date, end_date)
def get_data():
    pass


def earnings_stocks(stock_id, start_date, revenue):
    # end_date = format(datetime.date.today(), '%Y-%m-%d')
    end = datetime.date.today()
    try:
        start = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        stock = web.DataReader(stock_id, 'yahoo', start, end)
    except RemoteDataError as e:
        stock = web.DataReader(stock_id, 'yahoo', start_date, end)
    except (TypeError, ValueError) as e:
        return("""data does not match format '%Y-%m-%d'""")
    # except ValueError as e:
    #     raise e("""data does not match format '%Y-%m-%d'""")
    stock.fillna(method='ffill')
    close = stock.loc[:, "Close"]
    old_cost = close[0]
    profit = close.apply(profit_collum, args=(old_cost, revenue))
    new_revenue = profit.apply(revenue_collum, args=(revenue,))
    month_revenue = new_revenue.resample('M').mean()
    month_profit = profit.resample('M').mean()
    return month_revenue, month_profit


def total_earnings_profit(*args):
    return sum(list(args))


def total_earnings_revenue(*args):
    return sum(list(args))


# new_revenue = prof.apply(revenue_collum, args=(1200,))
