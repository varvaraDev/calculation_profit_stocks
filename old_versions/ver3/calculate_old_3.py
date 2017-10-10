def grouper_by_moth(df):
    """Return DataFrame aggregated by month and round."""
    # get_level_values return a vector of the labels for each location at a particular level
    return df.groupby([df.index.get_level_values(0)]+[pandas.Grouper(
                      freq='BM', level=1)]).mean().round(2)


def count_profit(df, parse, feild):
    """Calculate count purchased stocks by a given field."""
    profit = []
    for item in parse:
        df_stock = df.loc[slice(item.stock_id, item.stock_id), :]
        price = df_stock[feild][0]
        profit.append(
            (item.revenue / price) * (df_stock.Open - df_stock.Close)
            )
    return profit[0].append(profit[1:])
