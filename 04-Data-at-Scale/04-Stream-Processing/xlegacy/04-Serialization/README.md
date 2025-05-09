# 🎯 Goal

First of all, let's remember what an API is.

Here's a scenario

- I've written some code that does something useful for the world.
- Let's say it's written in Python.
- I'd like to make this code available and useful for other people than me.
- Even people who don't know Python.

**🤔 ⁉️ How do I do that?**

<details>
<summary markdown='span'>💡 Hint</summary>

They keyword here is `interface`.
</details>

That's what APIs or [Application Programming Interfaces](https://en.wikipedia.org/wiki/API) are for.

An API is here to delimit the bits of your code that you'd like to expose to the rest of the world 🌐

Ideally, the interface you create is language-agnostic, meaning it's accessible using Python, Rust, Go, C++, Ruby, Javascript, etc. And even web browsers and apps like Postman (because they use one of the programming languages mentioned earlier 😉).

We'll build some simple APIs, then more complex ones, for both formats that we discussed in the lecture:
  - For **JSON** - a HTTP API using the [popular and modern FastAPI library](https://fastapi.tiangolo.com/).
  - For **protobuf** - a [gRPC](https://grpc.io/) API.

### Before we start, let's discover the Python packages we'll use

Open your `pyproject.toml` file. Like all the other challenges, we're using Poetry to manage our dependencies. In this challenge, the packages doing the work are:

```toml
# to load CSVs
pandas = "^2.2.3"

# for the JSON HTTP API
fastapi = "^0.115.6"
uvicorn = "^0.34.0"

# for the Protobuf + gRPC part.
grpcio-tools = "^1.69.0"
```

This challenge will make heavy use of your IDE's capability (otherwise you may get lost)!
- Make sure VScode is using the correct `.venv` as Python Interpreter. It should be by default.
- Use **right-click** / **command-click** on your function calls and imports to navigate through imports rapidly!
- Use **ctrl-p** / **command-p** to navigate through files by name
- Use **ctrl-shift-R**/ **command-shift-r** to search for a symbol or character sequence globally!
- Use **View Split Editor** to view several files at once! gRPC requires working in a few files.

<br>

# 1️⃣ Warming up: A simple JSON HTTP API ⛏️

We'll start by creating the RESTful API in `api/rest_api.py`.

## 1.1. GET /time

Let's start simple, we want to return the current hour `h`, minute `m`, second `s`, broken down in a JSON that looks something like this.

```json
{
  "h": 10,
  "m": 3,
  "s": 1
}
```

❓ **Complete the imports, FastAPI object instantiation, decorators, and function body of `time()`**

When you think you have it working, test the API locally with:

```bash
uvicorn api.rest_api:app --host 0.0.0.0 --port 8000
```

And test by running `curl http://localhost:8000/time` in your terminal. You should see `{"h":22,"m":23,"s":40}` with your the current hour, minute, second (according to UTC time).

<br>

# 2️⃣ Protobuf + gRPC 🔧

We are going to recreate this API using protobuf + gRPC 💪. There are 4 steps that are necessary:
1. Create a `.proto` file where we define the service (function) and input/output variables (messages) to use
1. Compile the `.proto` file into Python code that amongst others takes care of the serialization/deserialization
1. Create the server code
1. Create the client-side code

## 2.1. Define our api/api.proto

❓**Create the messages and services for the `time` function that you created for the FastAPI, similarly as the example below. Do this in `api/protos/api.proto`.**

🤔 Context please? We start by defining the API that we want to create by creating a **service** in a `.proto` file. A service definition includes a **name** and a **list of methods** that the service supports. Each method has a name, a list of input parameters, and a list of output parameters.

For example, here's a `.proto` file with a service called `NumberStreamService` that has a single method called `GetNumbers`, which takes no input and returns a stream of int32 values (notice the `stream` keyword in front of `GetNumbersResponse`):

```javascript
syntax = "proto3";

// define your service
service NumberStreamService {
  rpc GetNumbers (GetNumbersRequest) returns (stream GetNumbersResponse) {}
}

// define service inputs parameters
message GetNumbersRequest {
}

// define service output parameters
message GetNumbersResponse {
  int32 value = 1;
}
```

👉 Your service should be called `TimeService` and is not a streaming one!

<details>
  <summary markdown='span'>🎁 Solution (to make sure you start correctly)</summary>

```javascript
syntax = "proto3";

// My first endpoint to get current time
service TimeService {
  rpc GetTime (TimeRequest) returns (TimeResponse) {}
}

message TimeRequest {
}

message TimeResponse {
  int64 h = 1;
  int64 m = 2;
  int64 s = 3;
}
```
</details>

<br>

## 2.2. Compile your .proto file

Use the **protoc** compiler. The **protoc** compiler reads the `.proto` file and generates code in the target language (in this case, Python) that provides the necessary classes and methods for interacting with the gRPC service defined in the `.proto` file.

❓ **Compile the `.proto` file with the following (deeply unpleasant) command**:

```bash
python -m grpc_tools.protoc \
    -Iapi/generated_proto=api/protos \
    --python_out=. \
    --grpc_python_out=. \
    api/protos/api.proto
```

Let's break down the parts of this command:
- `python -m grpc_tools.protoc` - is reaching into the python module `grpc_tools` and running a function `protoc` from the CLI.
- `-Iapi/generated_proto=api/protos` - is mapping the imports in our created python files to match our package structure
- `--python_out=.` - the location of one of our output files. Concatenated to our mapping.
- `--grpc_python_out=.` - the location of our second output file. Concatenated to our mapping.
- `api/protos/api.proto` - the `.proto` file we want to compile

Two files are created as a result.
- `api_pb2.py` containing classes for each custom **message** defined in the `.proto` file.
- `api_pb2_grpc.py` containing interfaces and classes for each **service** defined in the `.proto` file, including:
  - An **interface** for each service, with methods for each service method.
  - A **stub** class for each service that sends requests to the server and receives responses.
  - A **server** class for each service that receives requests from the client and sends responses.

It might not make much sense at the moment, but will become clearer later as you use them.

To prevent you from having to type that out again, we've make a command in your `Makefile` to help you out.

The generated code can indeed be imported into your Python code in the next step and be used to implement the server and client for your gRPC service.

<img src="https://storage.googleapis.com/lewagon-data-engineering-bootcamp-assets/datasets/movies/w1d3/exercises/day-3-protobuf-grpc-parts.png" width=800 />


❓ Have a look at the generated code in `api_pb2_grpc.py` and `api_pb2.py`. We'll be using the classes and methods in `api_pb2_grpc.py` to create our server and client.

👉 Let's move on to the `client` and `server` code now. We give you 2 options
- ❓**Guided option (if you need some help)**: Follow steps **2.3.** and **2.4.** below
- ❓**Not guided (better learning experience)**: Try to complete the two following files and run them side by side in two separate terminals:

```bash
python api/proto_rpc_server.py  # Should say "server started running"
python api/proto_rpc_client.py  # Should say "API client received: h:10 m:35 s:56"
```

## 2.3. Create the server code: api/proto_rpc_server.py

To implement the **server** for this service, you will need to define a method that takes a **request** object and and **returns** the desired response objects one at a time. Here's an example of how you might implement the GetNumbers method for the NumberStreamService:

```python
import streaming_pb2
import streaming_pb2_grpc
import grpc
from concurrent import futures
import time

class NumberStreamService(number_stream_pb2_grpc.NumberStreamServiceServicer):
    def GetNumbers(self, request, context):
        for i in range(1, 6):
            yield number_stream_pb2.GetNumbersResponse(value=i)
```

💡 Here we `yield` a return as we want to return a **stream of messages**. If you are not returning a stream, then just use the `return` keyword.

Once you have implemented the **service** class, you can create a **gRPC** server and add the service to it. With the FastAPI we were using **Uvicorn** for this. Using gRPC we can utilize the classes that were created when we compiled the `.proto` file.

```python
# Create a gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
streaming_pb2_grpc.add_NumberStreamServiceServicer_to_server(NumberStreamService(), server)
server.add_insecure_port('[::]:50051')
server.start()
print("start server")
server.wait_for_termination()
```

☝️ See how we are adding our service as the input to the `add_NumberStreamServiceServicer_to_server` method? You should have access to the equivalent `add_TimeServiceServicer_to_server` already available to your on `api_pb2_gprc.py` 🙂

❓ **It is your turn now to create the server side of your API for the `time` method in `api/proto_rpc_server.py`**

When you think you have it working, try to run the server by running the python file:

```bash
python api/proto_rpc_server.py # Should say "server started running"
```

## 2.4. Create the client code in `api/proto_rpc_client.py`

👇 Here's an example of how you might create a channel and a **stub** for the `NumberStreamService` and print the numbers received from the `GetNumbers` method:

```python
import grpc
import streaming_pb2
import streaming_pb2_grpc

channel = grpc.insecure_channel('localhost:50051')
stub = streaming_pb2_grpc.NumberStreamServiceStub(channel)

response_iterator = stub.GetNumbers(streaming_pb2.GetNumbersRequest())

for response in response_iterator:
    print(response.value)

channel.close()
```

❓ **Now it's your job to create the client-side code for your application!**

❓ **Try to run the server by running the python file**.

```bash
python api/proto_rpc_client.py # Should return "API client received: h:10 m:35 s:56"
```

<br>

# 3️⃣ Add a new "Rural" end-point

Let's step things up with a new endpoint that returns some data 🏋️‍♀️

## 3.1. Add endpoint in FastAPI

In your FastAPI app, add a `GET` endpoint `GET /country/:country/year/:year` that returns the `Rural population (% of total population)` for a given country and year. The data that is used is loaded from a `S3` bucket in `rural.py`. You need to use pandas to retrieve the value from the `Value` column given the year and country that is used as input variables for the API.

❓ In `api/rest_api.py` complete the `get_rural_population(country: str, year: int)` function to create a new endpoint. With the following requirements:
- Add the decorator: the endpoint should be `GET /country/<country>/year/<year>` - for example, if I wanted the rural population in Lithuania in 2012: `/country/Lithuania/year/2012`
- The data used is loaded from a `S3` bucket in `rural.py` - already provided
- You need to use pandas to filter the dataframe to retrieve the value from the `Value` column.
- Return the object as a python dictionary. Make sure that the value you are returning is a float, **not** a pandas Series or DataFrame.

If you want to download and look at the CSV to see what columns to filter/manipulate, you can use:

```bash
mkdir -p data && curl -o data/API-rural.csv https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W3D2-advanced-pipelines/API-rural.csv
```

<details>
<summary markdown='span'>💡 Hint</summary>

Check out the documentation about path parameters in FastAPI at [this link here](https://fastapi.tiangolo.com/tutorial/path-params/) and how to get access them.

Be aware that when you are testing your API that the `country` name input is case sensitive. Make sure you are querying the country name as it appears in the data, or add logic to your endpoint to handle it.
</details>

When you think you have it working, launch your RESTful API locally with:

```bash
uvicorn api.rest_api:app --host 0.0.0.0 --port 8001
```

And test the endpoint with `curl` or `localhost:8501/docs`

## 3.2. In gRPC

If you've reached this part, congratulations. You should have all the ingredients to make your gRPC API fancier.

### 3.2.1. api.proto

Let's start with the `api.proto`:

❓ **Add a second endpoint to your `api.proto` named `CountryYearService`**

```javascript
// My first endpoint to get current time
service TimeService{
  ...
}

...snip...

// My second endpoint to get share of rural population per country
service CountryYearService{
  ...
}
```

Make sure you define a **Request** and **Response** with the appropriate parameters.

<details>
<summary markdown='span'>💡 Hints</summary>

Start with a `CountryYearService` that takes the `CountryYearRequest` and returns `CountryYearResponse`

Add a Protobuf message with a `CountryYearRequest` that has a `country` and a `year` field.

And a `CountryYearResponse` that has one field `value`.
</details>

When you think you have it working, re-compile your `api.proto` with `make generate`. Have a look at your created `api_pb2_grpc.py` and `api_pb2.py` files.

### 3.2.2. rural_server.py

Let's create our **Server** - were we are doing the work and computation of this endpoint.

❓ **Complete the missing parts in `rural_server.py`**

💡 You don't have to add the TimeService to this **Server** if you don't want too. Creating multiple endpoints on the server side is a bit trickier with gRPC because, we the developer, need to handle routing logic.

When you're done, your server should start with:

```bash
python api/rural_server.py
```

### 3.2.3. rural_client.py

Time to create our client. Have a look at `api/rural_client.py` and you should see it partially filled. We need to pass data (strings in this case) to our endpoint, and we can do that with command line arguments. We've provided the necessary command line parsing.

❓ **Complete the `run_client(...)` function.**

The goal is to print the following line to the terminal: *"The percentage of the rural population in <country> in the year <year> was <some_value>%"*

Make sure to round the percentage to two decimal places!

### 3.2.4. All together

When you think you have everything working, open up two terminals side by side. In one terminal run:

```bash
python api/rural_server.py
```

In the next one test it out with:

```bash
python api/rural_client.py --country=Lithuania --year=2017
# The percentage of the rural population in Lithuania in the year 2017 was 32.48%
```

<br>

# 🏁 Finishing up

Congratulations if you've made it this far 🎉 Building gRPC + protobuf APIs isn't as common as RESTful APIs, but still a worthwhile knowing.

🧪 Confirm this challenge with:

```bash
make test
```

And don't forget to git add, commit, and push your code to Github to track your progress on Kitt!

<br>

# Going further

You could combine the two gRPC services, `GetTime` and `GetCountryYear` by extending the your existing `rural_client.py` and `rural_server.py`. This requires some additional logic to route the call, generally you don't want to do this on the client, either do it on the server, or if your API call volume is high enough, on a dedicated load balance.

A possible solution would be:
- **Client**:
    - Add an additional flag to the `parse_args()` function for `--service` for control flow
    - Adding another `run_client()` function named something different with the response for the `TimeService`
- **Server**: This requires creating:
    - A **CombinedService** class that inherits from both the `api_pb2_grpc.TimeServiceServicer` and `api_pb2_grpc.CountryYearServiceServicer` classes so it has access to both `GetTime` and `GetCountryYear` methods
    - An **Interceptor** class that intercepts the client request and routes it based on the passed `--service` flag.

Feel free to look in the solution files for `combined_client.py` and `combined_server.py` for an implementation.

<br>
