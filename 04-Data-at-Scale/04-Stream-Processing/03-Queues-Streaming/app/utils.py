import datetime
from typing import List, Tuple, Dict, Iterable

from apache_beam.transforms.core import CombineFn
import apache_beam as beam


def str2timestamp(str_datetime, fmt="%Y-%m-%d %H:%M:%S.%f"):
    """Converts a datetime string into a unix timestamp (number of seconds from 1/1/1970 00:00:00 excluding leap seconds)"""
    dt = datetime.datetime.strptime(str_datetime, fmt).replace(
        tzinfo=datetime.timezone.utc
    )
    return int(dt.timestamp())


class ExtractWindowTimestampKey(beam.DoFn):
    def process(self, element, window=beam.DoFn.WindowParam):
        """
        Takes an unkeyed element and attaches the window's start timestamp as the key.

        Output: (window_start_timestamp (str), element (list))
        """
        window_start_str = window.start.to_utc_datetime().strftime(
            "%Y-%m-%d %H:%M:%S.%f"
        )
        yield (window_start_str, element)


def aggregate_sensors(timestamp: str, sensor_values: List[Tuple[str,]]) -> Dict:
    """
    Aggregates sensor readings grouped by timestamp.

    Args:
        timestamp_values | str: timestamp
        sensor_values | List[Tuple[str,]]: iterable of [sensor, value,] pairs
            eg: [['AtmP', '996', '1000',], ['Temp', 6], ['AtmP, 1000], ...]

    Returns:
        dict: {'Timestamp': ..., 'AtmP': ..., 'Temp': ..., ...}
            - Key order not important
    """

    # Create a dictionary of {sensor: List[sensor values]} pairs:
    # {sensor1: [sensor1_val1, sensor1_val2], sensor2: [sensor2_val1, sensor2_val2], ...}
    agg = {}
    for sensor, value in sensor_values:
        if sensor not in agg:
            agg[sensor] = []
        agg[sensor].append(float(value))

        # Alternatively replace lines 48, 49, 50 with:
        # agg.setdefault(sensor, []).append(float(value))

    # Create a dictionary of {sensor: Float(mean sensor value)} pairs:
    # {sensor1: sensor1_mean_val, sensor2: sensor2_mean_val, ...}
    result = {}
    for sensor, values in agg.items():
        result[sensor] = sum(values) / len(values)

    # Add the timestamp to the output before returning
    result["Timestamp"] = timestamp
    return result
