"""This module for calculate profit and revenue."""
import pandas


def grouper_by_moth(df):
    """Return DataFrame aggregated by month and round."""
    return df.groupby([df.index.get_level_values(0)]+[pandas.Grouper(
                      freq='BM', level=1)]).mean().round(2)


def revenue_count(df, parse, feild):
    """Count revenue for each stock."""
    revenue = []
    for item in parse:
        r = df[feild].xs(item.stock_id) * df.count_stocks.xs(item.stock_id)
        i = df.profit.loc[slice(item.stock_id, item.stock_id), :] + r
        revenue.append(i)
    return revenue[0].append(revenue[1:])


def count_stock(stock, parse_data, feild):
    """Calculate count purchased stocks by a given field."""
    count = []
    for item in parse_data:
        count.append(
            item.revenue / stock[feild].loc[slice(
                item.stock_id, item.stock_id), :]
            )
    return count[0].append(count[1:])


def revenue_count_apply(s, parse, Open, count):
    """Count revenue for each stock."""
    revenue = []
    for item in parse:
        revenue.append(s.loc[slice(item.stock_id, item.stock_id), :] +
                       Open.xs(item.stock_id) * count.xs(item.stock_id))
    return revenue[0].append(revenue[1:])


def count_stock_apply(s, parse):
    """"""
    count = []
    for item in parse:
        count.append(
            item.revenue / s.loc[slice(item.stock_id, item.stock_id), :]
            )
    return count[0].append(count[1:])


def revenue_count_apply(s, parse, Open, count):
    revenue = []
    for item in parse:
        revenue.append(s.loc[slice(item.stock_id, item.stock_id), :] +
                       Open.xs(item.stock_id) * count.xs(item.stock_id))
    return revenue[0].append(revenue[1:])

def count_revenue_simpl(s, parse):
    """Add sum revenue."""
    revenue = []
    for item in parse:
            revenue.append(
            s.loc[slice(item.stock_id, item.stock_id), :] + item.revenue
                )
    return revenue[0].append(revenue[1:])
