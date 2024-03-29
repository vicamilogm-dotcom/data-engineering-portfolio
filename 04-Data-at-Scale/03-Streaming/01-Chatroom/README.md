# Queues, PubSub

When there is too much data to handle for our workers, when data flow needs to be managed, or processing scheduled, queues come to the rescue.

To decouple our applications, it is good practice to have them talk to one another through messages, and to have these messages managed by a queue 🚥.

A fun way to practice with queues is to replace machines by humans and build a chat application 🐦.

We'll build that in three steps:

1. We'll start with the open source, rock-solid message broker [RabbitMQ](https://www.rabbitmq.com/). Each student will build their own chat server and clients.

**V1 with RabbitMQ**

<img src="https://storage.googleapis.com/lewagon-data-engineering-bootcamp-assets/assets/chat-rabbitmq.png" width=600>

2. One of the students will open up their chat server for everyone else. When you'll connect to it you'll get subscribed to messages from everyone else!

## Our RabbitMQ server

Surprise surprise, we'll use Docker Compose to easily deploy RabbitMQ.

Follow the [Docker Hub documentation](https://hub.docker.com/_/rabbitmq) to add `rabbitmq:3.10.6-management` to the `docker-compose.yml`.

**Instructions:**

- We'll need to map ports 5672 and 15672.
- Set the environment variables `RABBITMQ_DEFAULT_USER` to `rmq` and `RABBITMQ_DEFAULT_PASS` must be read from the `.env`.

**Note** Your `.env` is read by `docker-compose` but not by your code when you run it directly from the terminal. When you run the `lwqueue/*.py` files in this exercise, make sure you have exported the environment variable(s) in your `.env` before with

```bash
direnv allow
```
or if you have changed the envs

```reload
direnv
```

Then run the server in the background with `docker compose up -d`.

You can check that it's up and running by going to the port 15672 in your web browser.

<details>
  <summary markdown='span'>💡 Hint</summary>

  You can start from the example of a Postgres image from previous days, and adapt it to RabbitMQ. The concepts are the same:
  - container image
  - container name
  - environment variables
  - ports
  - mounted volumes
</details>

**Note** On Docker Hub, there were two main flavors of the RabbitMQ Docker image. One was ending with `-management`, that's the one we picked. It adds a plugin that brings a management dashboard for our RabbitMQ server.

## Client and server code

Now that we've got our RabbitMQ instance running and accessible, let's work on the files `lwqueue/rabbitmq*.py` to receive messages from the queue (ie. our chat), and post to it.

The code is heavily inspired by the [official tutorial](https://www.rabbitmq.com/tutorials/tutorial-three-python.html). **Please start by reading it to understand the main concepts**.

By the end of this section we should be able to run:

```bash
python lwqueue/rabbitmq_subscriber.py --host localhost --port 5672 --rmq-username <RabbitMQ username> --rmq-password <RabbitMQ password> --mode print
```

to receive messages sent to our chat and print them out to the terminal.

We'll also add the file `lwqueue/rabbitmq_send_message.py` to send a message using

```bash
python lwqueue/rabbitmq_send_message.py --host localhost --port 5672 --rmq-username <RabbitMQ username> --rmq-password <RabbitMQ password> --username <your name> --message "<your message here>"
```

### Shared code

Let's get to work and start with the shared `rabbitmq.py` file. In the tutorial, notice that two files are created:

- [emit_log.py](https://github.com/rabbitmq/rabbitmq-tutorials/blob/master/python/emit_log.py) which is the equivalent of our (cleaner) `lwqueue/rabbitmq_send_message.py`
- [receive_logs.py](https://github.com/rabbitmq/rabbitmq-tutorials/blob/master/python/receive_logs.py), equivalent ot `lwqueue/rabbitmq_subscriber.py`.

Both share a common start, creating the connection to RabbitMQ. Grab this piece of code and adapt it for our function `get_connection(...)` in `lwqueue/rabbitmq.py`.

Because we protected our RabbitMQ server with a username and password, we'll need to pass credentials to the connection parameters. Can you find documentation on how to authenticate the connection and adapt the code accordingly?

<details>
  <summary markdown='span'>💡 Hint</summary>

  [Here](https://pika.readthedocs.io/en/stable/modules/parameters.html)'s how you'd do it.
</details>

By now, we have a connection that can be shared between `rabbitmq_send_message.py::send_message(...)` and `rabbitmq_subscriber.py::receive_messages(...)`. Notice how we use it at the beginning of both functions.

### Message sender

We've pre-filled `send_message(...)` in `lwqueue/rabbitmq_send_message.py`. Based on the [tutorial](https://www.rabbitmq.com/tutorials/tutorial-three-python.html), the command to publish the message is missing. We'll need you to add it. There's one tricky part though, the `message` variable in the tutorial is a string, while in our code the `message` variable, which we'd like to send, is a dictionary. How would you send it?

<details>
  <summary markdown='span'>💡 Hint</summary>

  Remember our course about serialization and serialize it to JSON.
</details>

Let's see if it worked:
- Run `python lwqueue/rabbitmq_send_message.py --host localhost --port 5672 --message "Hello world" --username $USER --rmq-username rmq --rmq-password $RABBITMQ_DEFAULT_PASS`.
- Navigate to [http://localhost:15672/#/exchanges](http://localhost:15672/#/exchanges)
- In the `exchanges` tab, do you see `chat`?
- Click on it and paste the URL into `tests.json`, `"chat"`
- Run `make test`, commit and push, to share your progress

**Did you notice a spike in the message rate when you sent the message?**

### The subscriber

Let's get to the hard part here, as we'll deal with callbacks, that sometimes can be hard to digest.

In the `receive_messages(...)` function of `lwqueue/rabbitmq_subscriber.py`, we've left out the bit that registers the callback, itself passed as the argument `on_message_callback`. **Fill it in.**

A callback here is a function with the signature

```python
def callback(channel: str, method, properties, body):
  # do stuff here
```

which is called every time a new message is received by the subscriber. We'll implement the simplest possible callback here, which simply prints the `"Received"` followed by the `body` value, to the console. Fill in the function `print_callback(...)` which was left empty.

Now, notice in the `main` function how `print_callback` is passed as the argument of `receive_messages`, **does it make sense?**

<details>
  <summary markdown='span'>💡 Hint</summary>

  We're building a flexible subscriber here, that can accept callbacks as parameters. First, we implement the simplest possible behavior, which is to just `print(...)` to the console the newest message received. In Python, this "behavior" is a function.

  Functions that are passed to other functions and called "on demand" are usually called **callbacks**.
</details>

Done? In two terminal windows, run

**The subscriber**

```bash
python lwqueue/rabbitmq_subscriber.py --host localhost --port 5672 --mode simple --rmq-username rmq --rmq-password $RABBITMQ_DEFAULT_PASS
```

**The publisher**

```bash
python lwqueue/rabbitmq_send_message.py --host localhost --port 5672 --message "Hello world" --username $USER --rmq-username rmq --rmq-password $RABBITMQ_DEFAULT_PASS
```

What happens?

## Optional (but nice!). Next, add a cool UI to it 🎨

The basic terminal is pretty boring isn't it? Let's display nicely messages we're receiving from other chatters using [Rich](https://rich.readthedocs.io/en/stable/live.html).

**Try out the [two top examples](https://rich.readthedocs.io/en/stable/live.html) to get familiar with Rich**

Now that you're familiar with Rich, we've pre-populated `lwqueue/ui.py` to create a new Rich table. It's missing the bit where messages are added as rows to the table. **Can you add it?**

Done?

Change the mode to `rich` in your subscriber, and send new messages from your publisher.

```bash
python lwqueue/rabbitmq_subscriber.py --host localhost --port 5672 --mode rich
```

Awesome, now we're ready to talk to other folks.

### Back to the management dashboard

When your subscriber is up, go to the `Queues` tab. Anything new?

You should see a new queue, which corresponds to your subscriber. Click on it and use the dashboard to publish a message to it. Observe the spike in the message rate.

By the way, did you get the message in your terminal?

## Now, chat with your group!

If you've reached this point, this means you've got RabbitMQ in a Docker network on port 5672, mapped to your host's port 5672. You can't share this port outside your host just yet because the firewall is blocking requests from outside it.

### Allow a port on GCP

- Go to the service `VPC Network`
- Click on `Firewall` on the left menu
- Click `CREATE FIREWALL RULE` (right next to `CREATE FIREWALL POLICY`)
  - Give it a name
  - Give it the target tag `rabbitmq-<your username>`
  - Source IPv4 ranges: `0.0.0.0/0` which means any IP can access it
  - Protocol and ports. On the internet, search whether the RabbitMQ protocol (AMQP) uses TCP or UDP (😄 can't give you all the answers!)
  - Once you've found the protocol and checked it, type `5672` in the `Ports` input
  - Click `CREATE`
- Now go back to your virtual machine and click `EDIT`
  - The target tag `rabbitmq-<your username>` given to your firewall rule above corresponds to a network target tag. Now look for `Network tags` and type `rabbitmq-<your username>`
  - Then click `SAVE` which will update your instance

Your RabbitMQ server should be open to the world!

### Share with the group

We wouldn't want to share our root user password though

❓ Create a user which is only allowed to send messages and that is it!

<details>
<summary markdown='span'>Solution 💡</summary>

```bash
docker exec -it <your rabbit mq container> rabbitmqctl add_user messaging_user abc123
docker exec -it <your rabbit mq container> rabbitmqctl set_permissions -p / messaging_user ".*" "" "^$"
```

</details>


Share the following with your mates (in Slack / Zoom / Teams):
- Your server IP address
- The RabbitMQ password over [Password Pusher](https://pwpush.com/), make sure you increase the number of views to 100 for everyone to be able to see it.

<details>
<summary markdown='span'>💡 How to send messages to a classmates server</summary>

```bash
python lwqueue/rabbitmq_send_message.py --host <classmates_vm_ip> --port 5672 --message <your_message> --username $USER --rmq-username <classmates_rmq_username> --rmq-password <classmates_rmq_password>
```

</details>


Now, are you receiving messages from your peers? No trash talking allowed... officially 😉!

### 🏁 Finish

We have a chatroom working but next we are not done here we want to create some analytics for our chatroom!
