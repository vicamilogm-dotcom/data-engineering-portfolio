import argparse
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import apache_beam.transforms.window as window
import pandas as pd

from app.utils import str2timestamp, strtime_window_rounded, aggregate_sensors








def run(subscription_name: str, output_table: str, interval=15.0, pipeline_args=None):
    with beam.Pipeline(
        options=PipelineOptions(
            pipeline_args,
            streaming=True,  # This time we are streaming ! PCollection are now "unbounded"
            save_main_session=True,
        )
    ) as pipeline:
        # pipeline steps to pull the data from pub/sub
        data = (
            pipeline
            pass  # YOUR CODE HERE
        )

        # pipeline steps to window the data
        windowing = (
            data
            pass  # YOUR CODE HERE
        )

        

        # pipeline steps to group and aggregate the data
        group = (
            windowing
            pass  # YOUR CODE HERE
        )

        group | "Print debug" >> beam.Map(lambda x: print(x))

        # pipeline steps to write to big query
        (
            group
            pass  # YOUR CODE HERE
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", dest="project")
    parser.add_argument("--subscription-name", dest="subscription_name")
    parser.add_argument("--interval", dest="agg_interval", default=15)
    parser.add_argument("--output-table", dest="output_table", default=False)

    args, pipeline_args = parser.parse_known_args()
    subscription_name = (
        f"projects/{args.project}/subscriptions/{args.subscription_name}"
    )

    run(subscription_name, args.output_table, args.agg_interval, pipeline_args)
