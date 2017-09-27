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
    new_cost = float(new_cost)
    profit_percent = (new_cost - old_cost) / new_cost
    profit = revenue * profit_percent
    return round(profit, 2)


def revenue_collum(profit, revenue):
    """Calculate revenue for every date for object Serial.

    Args:
        profit - values from result profit_collum
        revenue - dollars invested in share

    Return - update revenue with considering get profit

    """
    profit = float(profit)
    if profit == 0:
        return revenue
    revenue_new = profit + revenue
    return round(revenue_new, 2)


def profit_collum2(new_cost, old_cost, revenue):
    """Calculate profits for stock in procent.

    Args:
        new_cost - the value in the column 'Close' by table stock
        profit_percent - profit in percentage terms
        revenue - dollars invested in share

    Return
        profit - profit in USD terms

    """
    new_cost = float(new_cost)
    profit_percent = (new_cost - old_cost) / new_cost
    return round(profit_percent, 2)
