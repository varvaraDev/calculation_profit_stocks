* data_stock = web.DataReader(['GOOG', 'AAPL'], 'yahoo', '2017-01-01', retry_count=8)
* data_stock
* data_stock.head(10)
* data_stock2 = web.DataReader('GOOG', 'yahoo', '2017-01-01', retry_count=8)
* data_stock2
* data_stock2['ID'] = 'GOOG'                                                                                                             │
* data_stock2                                                                                                                            │
* data_stock2.index                                                                                                                      │
* data_stock2.columns                                                                                                                    │
* data_stock2.unstack                                                                                                                    │
* data_stock2.unstack()                                                                                                                  │
* data_stock2.stack()                                                                                                                    │
* data_stock2.reset_index()                                                                                                              │
* data_stock2.reset_index().set_index('Date', 'ID')                                                                                      │
* data_stock2.reset_index().set_index(['Date', 'ID'])                                                                                    │
* data_stock3 = web.DataReader('AAPL', 'yahoo', '2016-01-01', retry_count=8)                                                             │
* data_stock3['ID'] = 'AAPL'                                                                                                             │
* data_stock3 = data_stock3.reset_index().set_index(['Date', 'ID'])                                                                      │
* data_stock2 = data_stock2.reset_index().set_index(['Date', 'ID'])                                                                      │
* data_stock3                                                                                                                            │
* data_stock2 + data_stock3                                                                                                              │
* data_stock2.append(data_stock3)                                                                                                        │
* data_stock2.append(data_stock3).index                                                                                                  │
* data_stock2                                                                                                                            │
* data_stock2.index                                                                                                                      │
* f = data_stock2.append(data_stock3)                                                                                                    │
* f                                                                                                                                      │
* f['profit'] = f.Open - f.Close
* f
* f.profit
* f.profit.unstack()
* f.profit.unstack(level=0)
* f.profit.reset_index()


apple1 = data_stock3.reset_index().set_index(['ID', 'Date'])
apple1 = data_stock3.reset_index().set_index(['ID', 'Date'])
x = goog1.append(apple1)

# Различные срезы
x.xs('2017-09-25', level = 'Date')
x.loc['AAPL', :]
 x.loc[(slice(None), slice('2017-08-17', '2017-09-28')), :]
x.Close.unstack(level=0).resample('M').mean()


x.index.get_level_values(level=0)

def reindex(data_stock, id_stock, revenue):
    data_stock["count_stocks"] = round(revenue / data_stock.Open, 4)
    data_stock = data_stock.reset_index().set_index('Date', 'ID')
    data_stock = data_stock.groupby(pandas.Grouper(freq='BM')).mean()
    return data_stock


def main_func2(parse):
    """Main function for create a final DataFrame"""
    list_stock = []
    for item in parse:
        row = get_stock_data(item.stock_id, item.data_start)
        handle = handle_stock(row, item.stock_id, item.revenue)
        list_stock.append(handle)
    result = list_stock[0].append(list_stock[1:])
    # result['profit'] = result.Open - result.Close
    # result['revenue'] = result.revenue + result.profit
    return result

# if level = 0 ID and level = 1 Date
def grouper_by_moth(df):
    level_values = df.index.get_level_values
    return (df.groupby([level_values(0)]+[pandas.Grouper(freq='BM', level=-1)]).mean())


x.groupby([x.index.get_level_values(0)]+[pandas.Grouper(freq='BM', level=1)]).mean()
x.groupby([x.index.get_level_values(0)]+[pandas.Grouper(freq='BM', level=1)]).mean().round(2)


f.profit.unstack(level=1).sum(axis=1, skipna=True)

t_profit = final_result.profit.unstack(level=0).sum(axis=1, skipna=True)


 month = final_result.unstack(level=0).index
 month.to_period().to_native_types().tolist()
['{}'.format(str(item)) for item in month2.to_period().tolist()]


result.unstack(level=0).index.to_period().to_native_types().tolist()

final_result.index.levels[0].tolist()
['AAPL', 'GOOG']


def test(s):
    return s.xs('AAPL')
result.apply(test, axis=0)

Возращается DataFrame, при этом построчно (return работает 10 раз)
При axis=1 ошибка


result.apply(test, axis=0).profit


def test2(s):
    print(s.loc[slice('AAPL', 'AAPL'), :])
    print(s.loc[slice('GOOG', 'GOOG'), :])
    print(s.index)
    return s.loc[slice('AAPL', 'AAPL'), :] + 1200, s.loc[slice('GOOG', 'GOOG'), :] + 500


def test2(s):
    revenue = []
    revenue.append(s.loc[slice('AAPL', 'AAPL'), :] + 1200)
    revenue.append(s.loc[slice('GOOG', 'GOOG'), :] + 500)
    revenue.append(s.loc[slice('AMZN', 'AMZN'), :] + 500)
    return revenue[0].append(revenue[1:])


def count_revenue(s, parse):
    revenue = []
    for item for parse:
        revenue.append(s.loc[slice(item.stock_id, item.stock_id), :] + item.revenue)
    return revenue[0].append(revenue[1:])

result.profit.to_frame().apply(count_revenue, args = (parse,))
result.apply(count_revenue, args = (parse,)).profit


def count_revenue2(s, parse):
    revenue = []
    for item in parse:
        yield s.xs(item.stock_id)
ar.loc[slice('AAPL'), :]
ar.loc[slice('AAPL'), 'profit']


def xs_revenue(s, parse):
    revenue = []
    for item in parse:
        revenue.append(s.xs(item.stock_id) + item.revenue)
    return revenue[0].append(revenue[1:])

# Для получения периода (индеком становится дата)
# f.profit.unstack(level=1)

# Для получения среза по ID
# f.xs('GOOG', level='ID')
# Для получения total_profit
 # f.profit.unstack(level=1).sum(axis=1, skipna=True)

# groupby by date
# f.profit.reset_index()
# Alternatives aggregated by month
# return stock.resample('BM').mean()
# stock.groupby(pandas.TimeGrouper(freq='BM')).mean()
# (It's deprecated in favor of just pd.Grouper)
#  stocks.resample('M').mean()
