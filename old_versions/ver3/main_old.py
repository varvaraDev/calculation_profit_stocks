def aggregated_data_stocks(parse):
    """Main function for create a final DataFrame"""
    list_stock = []
    for item in parse:
        row = get_stock_data(item.stock_id, item.data_start)
        handle = handle_stock(row, item.stock_id, item.revenue)
        list_stock.append(handle)
    result = list_stock[0].append(list_stock[1:])
    # result['profit'] = result.Open - result.Close
    # result['revenue'] = result.revenue + result.profit
    # result['count_stocks'] = result.Close.to_frame().apply(
    #     count_stock, args=(parse,)
    #  )
    result['profit'] = result.count_stocks * (result.Open - result.Close)
    result['revenue'] = result.profit.to_frame().apply(
        revenue_count,
        args=(parse, result.Open, result.count_stocks)
     )
    return grouper_by_moth(result)


def handle_stock2(data_stock, id_stock, revenue):
    """Function add MultiIndex and column in DataFrame

    Args:
        data_stock (DateFrame) object by stock
        id_stock (string) ID stock
        revenue (float) investments in the purchase

    Return:
        DataFrame with two index - ID and Date, new column 'count stock'"""
    data_stock["count_stocks"] = revenue / data_stock.Close
    data_stock['profit'] = data_stock.count_stocks * (
                           data_stock.Open - data_stock.Close)
    data_stock['revenue'] = data_stock.profit + (
        data_stock.count_stocks * data_stock.Close
        )
    data_stock = data_stock.groupby(pandas.Grouper(freq='BM')).mean()
    data_stock['ID'] = id_stock
    return data_stock.reset_index().set_index(['ID', 'Date'])
