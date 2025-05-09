import pandas as pd


def load_rural_csv():
    data = pd.read_csv(
        "https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W3D2-advanced-pipelines/API-rural.csv"
    )
    return data
