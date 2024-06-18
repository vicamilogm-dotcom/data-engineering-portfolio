import os
import argparse
import apache_beam as beam
from apache_beam.io import ReadFromText, WriteToText
from apache_beam.options.pipeline_options import PipelineOptions

from app.utils import strtime_window_rounded, aggregate_sensors


class AggregateSensors(beam.DoFn):
    # (optional) DoFn subclassing implementation of "aggregate_sensors" mapping function
    pass  # YOUR CODE HERE


def run(
    file_path: str,
    output_fps_prefix: str,
    interval=15,
    bool_output_bq=False,
    pipeline_args=None,
):
    with beam.Pipeline(options=PipelineOptions(pipeline_args)) as pipeline:
        # data section
        data = (
            pipeline
            
        )

        windowing = (
            data
            
        )

        grouping = (
            windowing
            
        )

        # out
        (
            grouping
            
        )

        if bool_output_bq:
            output_bq_table = os.environ.get("BQ_TABLE", "")
            output_gcs_temp = os.environ.get("GCS_TEMP", "")
            (
                grouping
                
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--input", dest="file_path", default="data/sensors_latency.csv")
    parser.add_argument("--output", dest="output_prefix", default="data/output.txt")
    parser.add_argument("--interval", dest="agg_interval", default=15)
    parser.add_argument("--out-bq", dest="bool_out_bq", default=False)

    args, pipeline_args = parser.parse_known_args()

    run(
        file_path=args.file_path,
        output_fps_prefix=args.output_prefix,
        interval=args.agg_interval,
        bool_output_bq=args.bool_out_bq,
        pipeline_args=pipeline_args,
    )
