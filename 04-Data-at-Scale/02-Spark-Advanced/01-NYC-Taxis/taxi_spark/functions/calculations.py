from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def calculate_trip_duration(df: DataFrame) -> DataFrame:
    """
    Calculates the trip duration in minutes.
    Trip duration is calculated as the difference between 'Trip_Dropoff_DateTime'
    and 'Trip_Pickup_DateTime' in Unix timestamp format, divided by 60.

    Args:
        df (DataFrame): Input DataFrame with 'Trip_Dropoff_DateTime'
                        and 'Trip_Pickup_DateTime' columns.

    Returns:
        DataFrame: New DataFrame with a 'trip_duration' column added.
    """
    pass  # YOUR CODE HERE


def calculate_haversine_distance(df: DataFrame) -> DataFrame:
    """
    Calculates the haversine distance between start and end coordinates.
    Uses columns 'start_lat', 'start_lon', 'end_lat', 'end_lon' for calculations.
    The distance is calculated in kilometers.

    Args:
        df (DataFrame): Input DataFrame with 'start_lat', 'start_lon',
                        'end_lat', 'end_lon' columns.

    Returns:
        DataFrame: New DataFrame with a 'haversine_distance' column added.
    """
    pass  # YOUR CODE HERE
