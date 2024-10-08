import datetime
from typing import List, Tuple
import pandas as pd


def str2timestamp(str_datetime, fmt="%Y-%m-%d %H:%M:%S.%f"):
    """Converts a datetime string into a unix timestamp(number of seconds 1/1/1970 00:00:00)"""
    dt = datetime.datetime.strptime(str_datetime, fmt)
    epoch = datetime.datetime.utcfromtimestamp(0)
    return int((dt - epoch).total_seconds())


def strtime_window_rounded(str_datetime, window=15, fmt="%Y-%m-%d %H:%M:%S.%f"):
    """
    Converts a datetime to rounded datetime with a frequency window in sec
    """
    timestamp = str2timestamp(str_datetime, fmt)
    timestamp_rounded = (timestamp // window + 1) * window
    datetime_rounded = datetime.datetime.utcfromtimestamp(timestamp_rounded)
    return datetime_rounded.strftime(fmt)


def aggregate_sensors(timestamp: str, sensor_values: List[List[Tuple]]):
    """
    Transform:
    Tuple(timestample, List(sensor values))

    into

    Dict('Timestamp': str, 'AtmP': float32, 'Temp': float32, 'Airtight': float32, 'H20C': float32)

    Refer to the notebook in the previous challenge for how you could achieve this.

    e.g. in:
    ('2022-11-25 09:00:15.000000', [
        ['AtmP', 996.0840610169381],
        ['AtmP', 1032.610169381134],
        ['Airtight', 1248.5965933454158],
        ...)

    e.g out:
    {
        'Timestamp': '2022-11-25 09:00:15.000000',
        'AtmP': 991.1477661132812,
        'Temp': 9.778665542602539,
        'Airtight': 1248.5965933454158,
        'H20C': 12.37144075123452
    }
    """
    pass  # YOUR CODE HERE
