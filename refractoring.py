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
