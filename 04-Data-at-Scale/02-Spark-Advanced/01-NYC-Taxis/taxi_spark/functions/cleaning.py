import re
from pyspark.sql import DataFrame, functions as F


def remove_duplicates(df: DataFrame) -> DataFrame:
    """
    Removes duplicate rows based on all columns.

    Args:
        df (DataFrame): Input DataFrame

    Returns:
        DataFrame: New DataFrame with all duplicate rows removed.
    """
    pass  # YOUR CODE HERE


def handle_nulls(df: DataFrame) -> DataFrame:
    """
    Fills null values in specified columns with predefined constants.
    'Tip_Amt', 'Tolls_Amt', 'surcharge', 'mta_tax' are filled with 0.0
    'Rate_Code' is filled with -1.0
    'store_and_forward' is filled with -1.0

    Args:
        df (DataFrame): Input DataFrame

    Returns:
        DataFrame: New DataFrame with null values in specified columns replaced.
    """
    pass  # YOUR CODE HERE


def type_casting(df: DataFrame) -> DataFrame:
    """
    Casts 'Passenger_Count' to integer and 'Trip_Distance' to float.

    Args:
        df (DataFrame): Input DataFrame

    Returns:
        DataFrame: A new DataFrame with columns cast to specified types.
    """
    pass  # YOUR CODE HERE


def normalize_strings(df: DataFrame) -> DataFrame:
    """
    Trims and uppercases the 'vendor_name' and 'Payment_Type' columns.

    Args:
        df (DataFrame): Input DataFrame

    Returns:
        DataFrame: A new DataFrame with normalized string values.
    """
    pass  # YOUR CODE HERE


def format_dates(df: DataFrame) -> DataFrame:
    """
    Converts 'Trip_Pickup_DateTime' and 'Trip_Dropoff_DateTime' to timestamp format.

    Args:
        df (DataFrame): Input DataFrame

    Returns:
        DataFrame: A new DataFrame with dates converted to timestamps.
    """
    pass  # YOUR CODE HERE


def filter_coordinates(df: DataFrame) -> DataFrame:
    """
    Filters rows where coordinates are outside the valid range.
    (-180 <= Longitude <= 180, -90 <= Latitude <= 90)

    Args:
        df (DataFrame): Input DataFrame

    Returns:
        DataFrame: A new DataFrame with rows having valid coordinates.
    """
    pass  # YOUR CODE HERE


def rename_columns(df: DataFrame) -> DataFrame:
    """
    Renames all columns by replacing non-alphanumeric characters with underscores
    and converting the text to lower case.

    Args:
        df (DataFrame): Input DataFrame

    Returns:
        DataFrame: A new DataFrame with renamed columns.
    """
    pass  # YOUR CODE HERE
