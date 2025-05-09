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


# Optional Aggregation Challenge using a CombineFn
# For example implementation, check the docs and scroll to the bottom.
# https://beam.apache.org/documentation/transforms/python/aggregation/combineperkey/


class SensorAggregationFn(CombineFn):
    """
    A custom CombineFn to aggregate sensor readings per timestamp key..

    This class is used with `CombinePerKey` to group and reduce a set of sensor readings
    like ['AtmP', 996.08] into average values for each sensor within a time window.

    Input PCollection format:
        ('2022-11-25 09:00:15.000000', ['AtmP', 996.08])

    After grouping by key and combining:
        ('2022-11-25 09:00:15.000000', {'AtmP': 991.15, 'Temp': 9.77, ...})
    """

    def create_accumulator(self) -> Dict[str, List[float]]:
        """
        Initializes a new, empty accumulator.

        The accumulator is a dictionary where:
            - keys are sensor names (e.g., 'AtmP', 'Temp')
            - values are lists of float sensor values

        Returns:
            dict: An empty dictionary to collect sensor readings.
        """
        return {}

    def add_input(
        self, accumulator: Dict[str, List[float]], input_value: Tuple[str, float]
    ) -> Dict[str, List[float]]:
        """
        Adds a single input value to the accumulator.

        Args:
            accumulator (dict): The current dictionary of sensor -> list of values.
                eg: {
                        "AtmP": [996.0, 1000.0],
                    }
            input_value (list): A list like ['Temp', 6.0] representing one sensor reading.

        Returns:
            dict: The updated accumulator with the new value added.
                eg: {
                        "AtmP": [996.0, 1000.0],
                        "Temp": [6.0],
                    }
        """
        sensor, value = input_value
        if sensor not in accumulator:
            accumulator[sensor] = []
        accumulator[sensor].append(float(value))
        return accumulator

    def merge_accumulators(
        self, accumulators: Iterable[Dict[str, List[float]]]
    ) -> Dict[str, List[float]]:
        """
        Merges multiple accumulators into one. This is required for distributed processing.

        Args:
            accumulators | Iterable[Dict[str, List[Float]]]: A list of accumulators (i.e., dictionaries from each worker).
                eg: [{"AtmP": [996.0]}, {"AtmP": [1000.0], "Temp": [6.0]}]
        Returns:
            Dict[str, List[float]]: A merged dictionary combining all sensor readings across workers.
                eg: {"AtmP": [996.0, 1000.0], "Temp": [6.0]}
        """
        merged = {}
        for acc in accumulators:
            for sensor, value in acc.items():
                if sensor not in merged:
                    merged[sensor] = []
                merged[sensor].extend(value)
        return merged

    def extract_output(self, accumulator: Dict[str, List[float]]) -> Dict[str, float]:
        """
        Finalizes the output from the accumulator by computing the mean for each sensor.

        Args:
            accumulator (dict): The dictionary of sensor: list of float values.
                eg: {"AtmP": [996.0, 1000.0], "Temp": [6.0, 8.0]}

        Returns:
            dict: A dictionary of sensor: mean value, ready for output.
                eg: {"AtmP": 998.0, "Temp": 7.0}
        """
        output = {}
        for sensor, values in accumulator.items():
            output[sensor] = sum(values) / len(values)

        return output


class SensorAggregationIncrementalFn(CombineFn):
    def create_accumulator(self) -> Dict[str, Tuple[float, int]]:
        """
        Initializes a new accumulator.

        Returns:
            Dict[str, Tuple[float, int]]: An empty dictionary where keys are sensor names and
            values are tuples of (sum of values, count of values).
        """
        return {}

    def add_input(
        self, accumulator: Dict[str, Tuple[float, int]], input_value: Tuple[str, float]
    ) -> Dict[str, Tuple[float, int]]:
        """
        Adds a single sensor reading to the accumulator.

        Args:
            accumulator (Dict[str, Tuple[float, int]]): Current accumulator where each key is
                a sensor name and each value is a (sum, count) tuple.
            input_value (Tuple[str, float]): A tuple of sensor name and sensor value.

        Returns:
            Dict[str, Tuple[float, int]]: Updated accumulator with the new input included.
        """
        sensor, value = input_value
        if sensor not in accumulator:
            accumulator[sensor] = (0.0, 0)
        sum_val, count = accumulator[sensor]
        accumulator[sensor] = (sum_val + float(value), count + 1)
        return accumulator

    def merge_accumulators(
        self, accumulators: Iterable[Dict[str, Tuple[float, int]]]
    ) -> Dict[str, Tuple[float, int]]:
        """
        Merges multiple accumulators from parallel workers into a single accumulator.

        Args:
            accumulators (Iterable[Dict[str, Tuple[float, int]]]): An iterable of accumulators
                to be merged.

        Returns:
            Dict[str, Tuple[float, int]]: A single accumulator with combined (sum, count) values
            per sensor.
        """
        merged = {}
        for acc in accumulators:
            for sensor, (sum_val, count) in acc.items():
                if sensor not in merged:
                    merged[sensor] = (0.0, 0)
                m_sum, m_count = merged[sensor]
                merged[sensor] = (m_sum + sum_val, m_count + count)
        return merged

    def extract_output(
        self, accumulators: Dict[str, Tuple[float, int]]
    ) -> Dict[str, float]:
        """
        Computes the final average for each sensor from the accumulated (sum, count) data.

        Args:
            accumulator (Dict[str, Tuple[float, int]]): A dictionary with sensor names as keys
            and (sum, count) tuples as values.

        Returns:
            Dict[str, float]: A dictionary mapping each sensor name to its average value.
        """
        return {sensor: s / c for sensor, (s, c) in accumulators.items()}
