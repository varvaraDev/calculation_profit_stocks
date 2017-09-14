def revenue_profit(revenue, old_cost, new_cost):
    """Calculate profits and revenue for every date """
    profit_proc = (new_cost - old_cost) / new_cost
    profit = revenue*profit_proc
    revenue_new = revenue + profit
    print(profit, revenue_new)


def profit_collum(new_cost, old_cost, revenue):
    """Calculate profits and revenue for every date """
    new_cost = float(new_cost)
    if new_cost == 0:
        return 0
    profit_proc = (new_cost - old_cost) / new_cost
    profit = revenue*profit_proc
    return profit

# def calculate_profit(all_stock, stock, revenue):
#     def profit_collum(new_cost, old_cost, revenue):
#         """Calculate profits and revenue for every date """
#         new_cost = float(new_cost)
#         if new_cost == 0:
#             return 0
#         profit_proc = (new_cost - old_cost) / new_cost
#         profit = revenue*profit_proc
#         return profit

# old_cost = stock.Close[0]
# profit = close.apply(profit_collum, args=(old_cost, revenue))


def revenue_collum(profit, revenue):
    """Calculate profits and revenue for every date """
    profit = float(profit)
    if profit == 0:
        return 0
    revenue_new = profit + revenue
    return revenue_new


# profit = close.apply(profit_collum, args=(30.480000, 1200,))
# new_revenue.resample('M').mean()
# closeP = panel_data.loc[:,"Close"]
