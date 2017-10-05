* data_stock = web.DataReader(['GOOG', 'AAPL'], 'yahoo', '2017-01-01', retry_count=8)                                                    │
* data_stock                                                                                                                             │
* data_stock.head(10)                                                                                                                    │
* data_stock2 = web.DataReader('GOOG', 'yahoo', '2017-01-01', retry_count=8)                                                             │
* data_stock2                                                                                                                            │
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

        //     var array = {{id_stocks|tojson}}
        //     len = array.length
         //
        //  array.forEach(function(item, array) {
        //        series.push( {
        //            name: item,
        //            data: {{ result.xs(item, level='ID').Close.tolist()|tojson }},
        //            dashStyle: 'longdash'
        //        } );
        //     });
