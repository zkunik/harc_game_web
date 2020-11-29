from datetime import timedelta


def calculate_week(date):
    """
    Utility to calculate the week of the year, starting from saturday and formated 2020-W46
    """
    return (date + timedelta(days=2)).strftime('%Y-W%W')
