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
'Other versions (use functions)'


def count_stock_func(data_stock, parse):
    """Function for calculate count stock

    Return object Series for new column"""
    count_stocks = []
    for item in parse:
        price = data_stock.Close.xs(item.stock_id, drop_level=False)
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
            data_stock.profit.xs(
                item.stock_id, drop_level=False
             ) + item.revenue
         )
    return revenue[0].append(revenue[1:])


def count_profit_xs(df, parse):
    """Calculate profit collumn:
    Note use column count_stock
    count purchased stocks by a given field."""
    profit = []
    for item in parse:
        df_stock = df.xs(item.stock_id, drop_level=False)
        price = df_stock.Open[0]
        profit.append(
            (item.revenue / price) * (df_stock.Open - df_stock.Close)
         )
    return profit[0].append(profit[1:])


def revenue_other(df, parse):
    """Function count revenue for each stock.

    Not use collumn 'count_stock'"""
    revenue = []
    for item in parse:
        df_stock = df.xs(item.stock_id, drop_level=False)
        price = df_stock.Open[0]
        rev = df_stock.profit * (item.revenue / price) + item.revenue
        revenue.append(rev)
    return revenue[0].append(revenue[1:])
