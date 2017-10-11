"""This module for calculate profit and revenue."""


def profit_collum(new_cost, old_cost, revenue):
    """Calculate profits for stock.

    Args:
        new_cost - the value in the column 'Close' by table stock
        profit_percent - profit in percentage terms
        revenue - dollars invested in share

    Return
        profit - profit in USD terms

    """
    profit_percent = (new_cost - old_cost) / new_cost
    profit = revenue * profit_percent
    return profit


def revenue_collums(profit, revenue):
    """Calculate revenue for every date for object Serial.

    Args:
        profit - values from result profit_collum
        revenue - dollars invested in share

    Return - update revenue with considering get profit

    """
    return profit + revenue

# from calculate import profit_collum, revenue_collums
#     stock["profit"] = stock.Close.apply(
#         profit_collum,
#         args=(stock.Close[0], revenue,)
#     )
#
#     stock["profit"] = stock.Close.apply(
#         profit_collum,
#         args=(stock.Close[0], revenue,)
#     )


def revenue_other(df, parse, feild):
    """Function count revenue for each stock.
    Not use collumn 'count_stock'"""
    revenue = []
    for item in parse:
        df_stock = df.loc[slice(item.stock_id, item.stock_id), :]
        price = df_stock[feild][0]
        rev = df_stock.profit * (item.revenue / price) + item.revenue
        revenue.append(rev)
    return revenue[0].append(revenue[1:])


def count_profit_xs(df, parse, feild):
    """Calculate count purchased stocks by a given field."""
    profit = []
    for item in parse:
        df_stock = df.xs(item.stock_id, drop_level=False)
        price = df_stock[feild][0]
        profit.append(
            (item.revenue / price) * (df_stock.Open - df_stock.Close)
            )
    return profit[0].append(profit[1:])


def count_stock(df, parse, feild):
    """Calculate count purchased stocks by a given field."""
    count = []
    for item in parse:
        price = df[feild].loc[slice(item.stock_id, item.stock_id), :][0]
        count.append(
            item.revenue / price
            )
    return count[0].append(count[1:])


def count_one_stock(stock_id, revenue, feild):
    """Calculate count purchased stocks by a given field."""
    price = df[feild].loc[slice(stock_id, stock_id), :][0]
    count = revenue / price
    return count


def count_stock2(stock, parse_data, feild):
    """Calculate count purchased stocks by a given field."""
    count = []
    for item in parse_data:
        count.append(
            item.revenue / stock[feild].loc[slice(
                item.stock_id, item.stock_id), :]
            )
    return count[0].append(count[1:])


def revenue_count(df, parse, feild):
    """Count revenue for each stock."""
    revenue = []
    for item in parse:
        r = df[feild].xs(item.stock_id) * df.count_stocks.xs(item.stock_id)
        i = df.profit.loc[slice(item.stock_id, item.stock_id), :] + r
        revenue.append(i)
    return revenue[0].append(revenue[1:])


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
