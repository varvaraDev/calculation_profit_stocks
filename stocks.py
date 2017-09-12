import datetime
import pandas_datareader.data as web
from calculate import profit_collum, revenue_collum


# test1 = web.DataReader('GOOG', 'yahoo', start_date, end_date)

def earnings_stocks(stock_id, start_date, revenue):
    end_date = format(datetime.date.today(), '%Y-%m-%d')
    stock = web.DataReader(stock_id, 'yahoo', start_date, end_date)
    stock.fillna(method='ffill')
    close = stock.loc[:, "Close"]
    old_cost = close[0]
    profit = close.apply(profit_collum, args=(old_cost, revenue))
    new_revenue = profit.apply(revenue_collum, args=(revenue,))
    


# new_revenue = prof.apply(revenue_collum, args=(1200,))
