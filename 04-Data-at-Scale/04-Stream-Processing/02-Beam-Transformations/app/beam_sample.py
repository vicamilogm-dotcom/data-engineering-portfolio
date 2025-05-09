import os
import argparse
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.io import ReadFromText, WriteToText
from apache_beam.transforms.window import FixedWindows

from app.utils import (
    str2timestamp,
    aggregate_sensors,
    ExtractWindowTimestampKey,
)


def run(
    file_path: str,
    output_fps_prefix: str,
    interval: int = 15,
    bool_output_bq: bool = False,
    pipeline_args=None,
):
    options = PipelineOptions(pipeline_args)
    with beam.Pipeline(options=options) as pipeline:
        # Read input from CSV (or later, PubSub)
        data = (
            pipeline
            
        )

        # Assign Beam event timestamps and apply fixed-time windowing
        windowing = (
            data
            
        )

        # Group by key (window timestamp), then aggregate
        grouping = (
            windowing
            
        )

        # Write results to local file
        _ = (
            grouping
            
        )

        # Optionally write to BigQuery
        if bool_output_bq:
            output_bq_table = os.environ.get("BQ_TABLE", "")
            output_gcs_temp = os.environ.get("GCS_TEMP", "")
            _ = (
                grouping
                
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", dest="file_path", default="data/sensors_latency.csv")
    parser.add_argument("--output", dest="output_prefix", default="data/output.txt")
    parser.add_argument("--interval", dest="agg_interval", type=int, default=15)
    parser.add_argument("--out-bq", dest="bool_out_bq", action="store_true")

    args, pipeline_args = parser.parse_known_args()

    run(
        file_path=args.file_path,
        output_fps_prefix=args.output_prefix,
        interval=args.agg_interval,
        bool_output_bq=args.bool_out_bq,
        pipeline_args=pipeline_args,
    )
