"""This module for calculate profit and revenue."""
import pandas


def grouper_by_moth(df):
    """Return DataFrame aggregated by month and round.

    Args:
        df (DateFrame) frame for grouping
        id_index (Index) first-level index by df (id stocks)
        group_by_month (TimeGrouper) specification for a groupby instruction

    Return:
        DateFrame group by month (mean) and rounding by 2

    """
    id_index = df.index.get_level_values(0)
    group_by_month = pandas.Grouper(freq='BM', level=1)
    # get_level_values return a vector of the labels for each location at a
    # particular level
    return df.groupby([id_index, group_by_month]).mean().round(2)


def count_revenue_apply(s, parse):
    """Create column revenue.

    Note:
        Add revenue by stock in profit. For apply

    Args:
        s (Serias) input table
        revenue (list) list for store data by each stock

    Return:
        Aggregated Serias by each stock

    """
    revenue = []
    for item in parse:
            revenue.append(
                s.xs(item.stock_id, drop_level=False) + item.revenue
                )
    return revenue[0].append(revenue[1:])


'**********************************************************************'
'Other versions'

def count_stock_func(data_stock, parse, feild_price):
    """Function for calculate count stock

    Return object Series for new column"""
    count_stocks = []
    for item in parse:
        price = data_stock[feild_price].xs(item.stock_id, drop_level=False)
        print
        count = item.revenue / price[0]
        c = pandas.Series(count, index=price.index)
        count_stocks.append(c)
    return count_stocks[0].append(count_stocks[1:])


def count_revenue_func(data_stock, parse):
    """Create column revenue.

    Note:
        Add revenue by stock in profit. For apply

    Args:
        s (Serias) input table
        revenue (list) list for store data by each stock

    Return:
        Aggregated Serias by each stock

    """
    revenue = []
    for item in parse:
            revenue.append(
                data_stock.profit.xs(item.stock_id, drop_level=False) + item.revenue
                )
    return revenue[0].append(revenue[1:])



def count_profit_xs(df, parse, feild):
    """Calculate profit collumn:
    count purchased stocks by a given field."""
    profit = []
    for item in parse:
        df_stock = df.xs(item.stock_id, drop_level=False)
        price = df_stock[feild][0]
        profit.append(
            (item.revenue / price) * (df_stock.Open - df_stock.Close)
            )
    return profit[0].append(profit[1:])


def revenue_other(df, parse, feild):
    """Function count revenue for each stock.

    Not use collumn 'count_stock'"""
    revenue = []
    for item in parse:
        df_stock = df.xs(item.stock_id, drop_level=False)
        price_buy = df_stock[feild][0]
        rev = df_stock.profit * (item.revenue / price_buy) + item.revenue
        revenue.append(rev)
    return revenue[0].append(revenue[1:])


def count_stock_change(stock, parse_data, feild):
    """Calculate count purchased stocks by a given field.
    If count stock is changing every day"""
    count = []
    for item in parse_data:
        count.append(
            item.revenue / stock[feild].xs(item.stock_id, drop_level=False)
            )
    return count[0].append(count[1:])


def revenue_count(df, parse, feild):
    """Calculate revenue for each stock by count stoks
    1 step - calculate new revenue = count * price (ex. Close)
    2 step - new revenue add profit
    """
    revenue = []
    for item in parse:
        r = df[feild].xs(item.stock_id, drop_level=False) * df.count_stocks.xs(item.stock_id,  drop_level=False)
        i = df.profit.xs(item.stock_id, drop_level=False) + r
        revenue.append(i)
    return revenue[0].append(revenue[1:])


def revenue_count_apply(s, parse, Open, count):
    """Count revenue for each stock."""
    revenue = []
    for item in parse:
        revenue.append(s.xs(item.stock_id, drop_level=False) +
                       Open.xs(item.stock_id) * count.xs(item.stock_id))
    return revenue[0].append(revenue[1:])



def revenue_count_apply(s, parse, Open, count):
    revenue = []
    for item in parse:
        revenue.append(s.loc[slice(item.stock_id, item.stock_id), :] +
                       Open.xs(item.stock_id) * count.xs(item.stock_id))
    return revenue[0].append(revenue[1:])
