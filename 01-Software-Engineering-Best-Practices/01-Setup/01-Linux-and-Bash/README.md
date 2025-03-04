# 🎯 Goal

The goal of this exercise is to create a **background service** on your virtual machine. We will write a shell script which checks whether you are connected via ssh and if not shutdown your VM in order to **prevent unwanted spending by leaving the vm running overnight!**

We will cover:
- The basics of services
- Creating a script to check if a user is connected via ssh, if there are no users then shutdown.
- Creating a service and that will run as a background process and a timer that will execute that service.
- Explore cronjobs as an alternative way to schedule operations.

<br>

# 1️⃣ Basics of services

A **service** in linux is a program that runs in the background outside of users which are not intended to be directly interacted with most of the time (sometimes they are also referred to as **Daemons**).

🔎 Lets see which ones are currently on the virtual machine:

```bash
systemctl list-units --type=service
```

You'll get a huge list of services let reduce it to just the currently running ones!:

```bash
systemctl list-units --type=service | grep running
```

❗️ Two important bash motifs are shown in this command:

**The pipe `|`**, which takes the standard output of one command and passes it as the input to the next one!
This is easy to confuse with passing it as an argument, but for example if we run:
```
echo 5 | echo
```
We get nothing as the standard input does not affect echo.

**[grep](https://www.gnu.org/software/grep/manual/grep.html)** searches the input it receives for a pattern. In this example grep searches the output of `systemctl list-units --type=service` for lines with `running` in them and returns only the lines matching the pattern.

From our command above and you will notice a couple of services that we are using already, the `ssh.service` is what is running in the background to allow SSH to operate. **You'll also see two things we have installed, docker and postgres, which both run in the background as services!**

If you had a lot more services and it was hard to see what was running. You could also use `grep` to check whether postgres was there for example!

<br>

# 2️⃣ Creating a script

❓ Let's start by creating a `check_ssh.sh` script which checks whether any users are currently connected, `echo` if there are and otherwise `poweroff` the VM!

📚 Some things worth exploring in relation to the script if you are not familiar with bash scripts:
- Start with `#!/bin/bash`. This is commonly called a [shebang](https://en.wikipedia.org/wiki/Shebang_(Unix)). It tells your computer that this file should be run using `bash`
- Go back to the lecture and check the control flow syntax there!
- Use `ss | grep "tcp.*ssh"` to check for SSH users

<details>
<summary markdown='span'>Solution</summary>

```bash
#!/bin/bash
connections=$(ss | grep "tcp.*ssh" | wc -l)
if [[ $connections > 0 ]]
then
    echo "Hey it looks like someone is connected"
else
    poweroff
fi
```
</details>

❓ Let's now make `check_ssh.sh` executable (`x`):

```bash
chmod +x check_ssh.sh
```
And now if you run it:
```bash
./check_ssh.sh
```

You should see that someone is connected!

❗️ **The command we just used, `chmod`, can do more than just make a file executable**. It also affects who can read, write, and execute files! Bookmark this [great article](https://www.computerhope.com/unix/uchmod.htm) for later if you want to learn a bit more about this concept.
<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W1D5/010102-file-permissions-and-ownership-in-linux.png" width=400>

❓ Lets move our script into `/usr/local` before we move on.

You might notice you get permission denied when trying to move the files into the folder you can fix this with sudo (💡 a useful trick if you forget a sudo is running `sudo !!` runs the previous command but with `sudo` prepended).You need this because only the root user can edit the root directory (along with everything on the system). Running `sudo` allows you to imitate the root user to run one command (a more in-depth look at [root](http://www.linfo.org/root.html)). This control over absolutely everything on the system is one of the most powerful things about linux. But you also must be careful not to overwrite key files, as there is a lack of guard rails.

<details>
  <summary markdown='span'>💡 Why /usr/local</summary>

If you want a quick explanation of most of the folders in the root directory (i.e. the highest folder in the system) this 2 min video explains the [linux filesystem](https://www.youtube.com/watch?v=42iQKuQodW4) at a high level.

</details>

<br>

# 3️⃣ Creating a service and timer

There is a few components to creating the service and executing it. Lets get going!

## 3.1. Creating a service

We need something to trigger our script, this is where **services** come in!

❓ Start off by creating a `check_ssh.service` file which triggers our script:

<details>
<summary markdown='span'>💡 Service example</summary>

```bash
[Unit]
Description=some description

[Service]
ExecStart=/bin/bash /usr/local/test.sh

[Install]
WantedBy=multi-user.target
```
</details>

## 3.2. Creating a timer

❓ Now create a `check_ssh.timer` file to trigger our service every 60 seconds and to commence 5 minutes after we boot up the Virtual machine - we don't want it to be so short that it turns off before you can connect!

<details>
<summary markdown='span'>💡 Timer example</summary>

```bash
[Unit]
Description=some description

[Timer]
OnUnitActiveSec=60s
OnBootSec=300s

[Install]
WantedBy=timers.target
```
</details>

## 3.3. Running the service

❗️ **Move these `check_ssh.service` and `check_ssh.timer` in the `/etc/systemd/system` directory**.

Now you can run `sudo systemctl daemon-reload` to make your service files available.

Run `sudo systemctl start <your_service>.service` to run the service once and check it does what you want it to. Then run `systemctl status <your_service>.service` to check if it is running! If you want more detailed logs you can use `sudo journalctl -r -u check_ssh` to see every output.

To use the timer **here are the key commands from systemctl**:
- `start` (starts the service/timer)
- `stop` (stops it)
- `enable` (always start on reboot but does not start now without --now)
- `disable` (stop it starting on reboot)

So to get our to run permanently we would use:
```bash
sudo systemctl enable --now <your_service>.timer
```

❗️ In general we do not want to have the service running all the time. Imagine turning on your VM and the service turns it back off before you get a chance to connect! So let us use a different approach! Disable the service and move on to next section.

<br>

# 4️⃣ Cron

Cron is an alternative way of running commands at a **specific time** of day, there are pros and cons to both but it is good to understand both. Cron is good for running short scripts at a particular time whereas services are much better for long running processes or process that have to be executed very often!

Let's open the crontab that keep track of cron jobs

```bash
sudo crontab -e
```
❓ This will open a file where you should write a line starting your service at a particular time! Now you need to add a line to start our `check_ssh.timer`!

The syntax for cron is a little strange but for instance, to run `echo` once a day at 10pm you would write:

```bash
0 22 * * * echo "I'm going to be printed every day at 10pm"
```

This [website](https://crontab.guru/#0_20_*_*_*) is great for checking your syntax!

<details>
  <summary markdown='span'>💡 crontab solution</summary>

```bash
0 22 * * * systemctl start check_ssh.timer
```

</details>

<br>

# 🏁 Finishing up

Services and cron are two powerful tools in the linux arsenal, here we could have achieved our goal with either on their own but it is useful to know both in case only one is appropriate!

🏁 We now have a cron which starts a timer running on our to check if anyone is connected and if not shut it down, stopping us spending too much money by accidentally leaving it on overnight!

<br>

# Alternative crontab solution without services

The above crontab solution uses the flow of:
- Start a background `check_ssh.timer` on a cron schedule
- The `check_ssh.timer` executes the `check_ssh.service` based on it's own schedule (e.g. every 120 seconds)
- `check_ssh.service` executes a shell script: `check_ssh.sh`
- `check_ssh.sh` checks if a user is connected by ssh.
  - If yes: do nothing.
  - If no: shutdown.

By using crontab, we can remove a few layers of abstraction to execute only the shell script, `check_ssh.sh`, on a cron schedule. For example:

```bash
*/15 * * * * /usr/local/check_ssh.sh
```

Will execute the shell script every 15 minutes of every hour of every day (when the virtual machine is on).

<br>
