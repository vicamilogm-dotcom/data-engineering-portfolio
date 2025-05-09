import argparse
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.transforms.window import FixedWindows
from apache_beam.transforms import window, trigger

from app.utils import (
    str2timestamp,
    aggregate_sensors,
    ExtractWindowTimestampKey,
)


def run(
    subscription_name: str,
    output_table: str,
    interval: int = 15,
    pipeline_args=None,
):
    options = PipelineOptions(
        pipeline_args,
        streaming=True,
        save_main_session=True,
    )
    with beam.Pipeline(options=options) as pipeline:
        data = (
            pipeline
            
        )

        # Assign Beam event timestamps and apply fixed-time windowing
        windowing = (
            data
            # DELETE_BEGIN
            | "Attach Timestamps"
            >> beam.Map(
                lambda row: beam.window.TimestampedValue(
                    [row[0], row[1]], str2timestamp(row[2])
                )
            )
            | "Apply Windows"
            >> beam.WindowInto(
                FixedWindows(interval),
                # trigger=trigger.Repeatedly(trigger.AfterProcessingTime(1 * 15)),
                # allowed_lateness=1800,
                # accumulation_mode=trigger.AccumulationMode.DISCARDING,
            )
            | "Attach Timestamp key" >> beam.ParDo(ExtractWindowTimestampKey())
            # DELETE_END
        )

        # Group by key (window timestamp), then aggregate
        grouping = (
            windowing
            
        )

        # Print debug - feel free to comment out
        _ = grouping | "Print debug" >> beam.Map(lambda element: print(element))

        # Stream to BigQuery
        _ = (
            grouping
            
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
