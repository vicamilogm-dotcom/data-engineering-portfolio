# 🎯 Goal

For the Recap there is two options:
1. If students get to the deploy section of `03-Queues-Streaming`, it is recommended to go through it.
2. A more efficient aggregation method using `CombinePerKey` instead of `GroupByKey` + `MapTuple`.
3. How we deal with late arriving data.

<br>

# 1️⃣ CombinePerKey

In challenges today you used **GroupByKey** to aggregate your data, which is a fantastic way to aggregate data, but it has limitations. When we're processing windowed data in beam, elements are grouped by **key** and by **window**.

**GroupByKey** is not **window aware**, it is purely aggregating based on the key of the element. There is a more efficient, but somewhat more involved, way of aggregating data using **CombinePerKey**.

**CombinePerKey** knows that it is operating in a window context and can automatically aggregate values within their window using a mechanism called *accumulators*. But how does this make it more efficient than **GroupByKey**?

**CombinePerKey** collects values in multiple accumulators per window, each accumulator can combine values earlier in parallel (before shuffling), merge accumulators in parallel, then emit results incrementally.

💡 An analogy to help illustrate this could be:
- **GroupByKey + MapTuple** is like gathering all your receipts for a month in a box, then calculating your monthly expenses at the end.
- **CombinePerKey** is like totalling each day's expenses **as you go**, and then only combining the daily totals at the end of the month.

This has real benefits in terms of compute:
- Low memory usage per key - incremental reduce (aggregation) instead of a single reduce operation
- Higher network efficiency and highly parallelised - **GroupByKey** assigns all the data with the same key to the same worker. **CombinePerKey** can have multiple accumulators across different workers. If you have lots of data points per key, this is a big saving.

Let's see how to implement it in code 🚀

<br>

# 2️⃣ CombinePerKey implementation

In our `grouping` step, instead of:

```python
windowing
    | "Group By Key" >> beam.GroupByKey()
    | "Aggregate Sensors" >> beam.MapTuple(aggregate_sensors)
```

We'll instead use:

```python
windowing
    | "Combine Per Window" >> beam.CombinePerKey(SensorAggregationFn())
    | "Reformat and add Timestamp"
    >> beam.Map(
        lambda element, window=beam.DoFn.WindowParam: {
            "Timestamp": element[0],
            **element[1],
        }
    )
```

Let's break down what is happening 🚀

## 2.1. Combine Per Window

To use **CombinePerKey** we need to pass a the custom **SensorAggregationFn**. This is an class that has been implemented in `utils.py` and inherits from the the `CombineFn` class.

Looking at the documentation for **CombinePerKey** at this [link here 🔗](https://beam.apache.org/documentation/transforms/python/aggregation/combineperkey/#example-5-combining-with-a-combinefn). Each `CombineFn` sub-class needs to have four components:
1. `create_accumulator` - This will return a new empty dictionary, an appropriate data structure to hold our elements
2. `add_input` - Logic for adding a single data point to a single accumulator
3. `merge_accumulators` - Logic for merging accumulators together
4. `extract_output` - Logic for extracting our output, this method is called only once per key.

You should be able to see the logic of the `aggregate_sensors` function that you implemented in the challenges in the `SensorsAggregationFn` class.

❗ Note that we can't compute the mean in `add_input` and `merge_accumulators` because averaging is **not associative**:

```python
avg([1, 2, 3]) != avg(avg([1, 2]), avg([3]))
```

So we need to leave it until `extract_output`. If your grouping was both associative and commutative, then you could do so.

💡 Because we're computing the mean, we could make this even more efficient by altering the logic in `add_input` and `merge_accumulators` to store the **sum** and **count** of values per sensor. So we would be storing a single value instead of a list of values. Feel free to look at the `SensorAggregationIncrementalFn` class for an implementation. This is not a universal solution, your aggregations will depend on the problem you are trying to solve.

## 2.2. Reformat and add Timestamp

The **Reformat and add Timestamp** step is just rearranging our element data structure.

```python
| "Reformat and add Timestamp"
    >> beam.Map(
        lambda element, window=beam.DoFn.WindowParam: {
            "Timestamp": element[0],
            **element[1],
        }
    )
```

The output data from our `CombinePerKey` is in the format:

```bash
('2025-05-09 15:58:15.000000', {'AtmP': 984.8934619721473, 'Temp': 8.35422664362706, 'Airtight': 1247.6760974211468, 'H2OC': 9.528452207274047})
('2025-05-09 15:58:30.000000', {'Airtight': 1205.0739651489978, 'AtmP': 988.4049677122812, 'Temp': 7.154916057218433, 'H2OC': 10.658445932270217})
...
```

And we want it in the format:

```bash
{'Timestamp': '2025-05-09 16:01:15.000000', 'AtmP': 990.298632428676, 'H2OC': 12.293422525803892, 'Airtight': 1215.4818594403737, 'Temp': 6.5178352854289585}
{'Timestamp': '2025-05-09 16:01:30.000000', 'Temp': 10.209584496077012, 'AtmP': 991.6536900338115, 'H2OC': 10.869797721480147, 'Airtight': 1227.7430424657368}
...
```

We have taken the **key**, and used the splat (or [dictionary unpacking 🔗](https://docs.python.org/3/reference/expressions.html#dictionary-displays)) operator to reformat our data from a tuple to a dictionary.

## 2.3. Specifying Window Triggers

Because we are now using a window aware aggregation, we also need to make a minor change to the **Apply Windows** step.

```python
| "Apply Windows"
>> beam.WindowInto(
    FixedWindows(interval),
)
```

And add some triggers to the window with the following:

```python
| "Apply Windows"
>> beam.WindowInto(
    FixedWindows(interval),
    trigger=trigger.Repeatedly(trigger.AfterProcessingTime(1 * 15)),
    allowed_lateness=1800,
    accumulation_mode=trigger.AccumulationMode.DISCARDING,
)
```

<br>

# 3️⃣ Optional - Building for late arriving data

Because we are working with message queues, there can be late arriving data, or data that arrives later than it's 15 second window. We can deal with this by adding a few keyword arguments to the **Apply Windows** section of **Windowing**. Currently we have:

```python
| "Apply Windows"
>> beam.WindowInto(
    FixedWindows(interval),
)
```

By adding a few extra arguments like:

```python
| "Apply Windows"
>> beam.WindowInto(
    FixedWindows(interval),
    # Add custom triggers
    trigger=trigger.AfterWatermark(early=trigger.AfterProcessingTime(15)),
    allowed_lateness=60, # allowed lateness in seconds
    accumulation_mode=trigger.AccumulationMode.DISCARDING,
)
```

- Use `DISCARDING` because each window should be self contained
- If new data shows up, Beam will re-open the window (if within `allowed_lateness`)
- The `trigger.AfterWatermark(early=trigger.AfterProcessingTime(15))` adds an early trigger that will:
    - Fire early(once), 15 seconds after the first element in each window arrives
    - Then fire again when the watermark passes (default behaviour).
    - Possible fire again if late data arrives, depending on `allowed_lateness`

The **watermark** is Beams best guess of the current event time. When we say a window is firing, that is when Beam will emit a result from a window.

# 4️⃣ Run to make sure it works!

Either locally with:

```bash
python app/subscriber_beam.py \
    --id $PROJECT_ID \
    --subscription-name $SUBSCRIPTION_NAME \
    --output-table $BQ_TABLE
```

Or deploy onto DataFlow with:

```bash
poetry build
```

```bash
python app/subscriber_beam.py \
    --id $PROJECT_ID \
    --subscription-name $SUBSCRIPTION_NAME \
    --output-table $BQ_TABLE \
    --runner DataflowRunner \
    --project $PROJECT_ID \
    --streaming \
    --temp_location $BUCKET_NAME/temp \
    --staging_location $BUCKET_NAME/staging \
    --extra_package dist/beam_recap-0.1.0-py3-none-any.whl \
    --region europe-west1
```

And don't forget to start the publisher:

```bash
python app/publisher.py
```

Wait a minute and have a look at your data in BigQuery!

<br>

# 🏁 Finishing up

Combining distributed computing and real time data streams is tricky. If this interests your, we strongly encourage you to dig deeper!
