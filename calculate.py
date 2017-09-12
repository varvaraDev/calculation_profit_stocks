def revenue_profit(revenue, old_cost, new_cost):
    """Calculate profits and revenue for every date """
    profit_proc = (new_cost - old_cost) / new_cost
    profit = revenue*profit_proc
    revenue_new = revenue + profit
    print(profit, revenue_new)


def profit_collum(new_cost, old_cost, revenue):
    """Calculate profits and revenue for every date """
    profit_proc = (new_cost - old_cost) / new_cost
    profit = revenue*profit_proc
    return profit

# prof = z.apply(profit_collum, args=(old_cost, revenue))


def revenue_collum(profit, revenue):
    """Calculate profits and revenue for every date """
    revenue_new = profit + revenue
    return revenue_new


def profit(new_cost, **kwargs):
    old_cost = kwargs.get('old_cost')
    revenue = kwargs.get('revenue')
    profit_proc = (new_cost - old_cost) / new_cost
    profit = revenue*profit_proc
    return profit


# profit = close.apply(profit_collum, args=(30.480000, 1200,))
# new_revenue.resample('M').mean()
# closeP = panel_data.loc[:,"Close"]
