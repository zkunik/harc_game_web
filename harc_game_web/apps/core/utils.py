from collections import defaultdict
from datetime import timedelta
import math


def calculate_week(date):
    """
    Utility to calculate the week of the year, starting from saturday and formated 2020-W46
    """
    return (date + timedelta(days=2)).strftime('%Y-W%W')


def round_half_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n*multiplier + 0.5) / multiplier


def default_to_regular(d):
    if isinstance(d, defaultdict):
        d = {k: default_to_regular(v) for k, v in d.items()}
    return d
