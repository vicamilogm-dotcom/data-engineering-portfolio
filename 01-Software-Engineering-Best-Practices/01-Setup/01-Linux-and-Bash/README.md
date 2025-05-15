# 🎯 Goal

The goal of this exercise is to implement an automated way to turn off your VM when you aren't connected to it to **prevent unwanted spending by leaving the VM running overnight!**

To achieve this we will:
- We'll also take a quick look at Linux **services** (or daemons), which are programs running in the background.
- Create a **bash script** to check if a user is connected via SSH, if there are no users then the VM will shutdown.
- Automatically run this script on schedule with some basic orchestration with **cronjobs**

<br>

# 1️⃣ Basics of services

A **service** in linux is a program that runs in the background outside of users which are not intended to be directly interacted with most of the time. They are sometimes referred to as **daemons**.

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
```bash
echo 5 | echo
```
We get nothing as the standard input does not affect echo.

**[grep](https://www.gnu.org/software/grep/manual/grep.html)** searches the input it receives for a pattern. In this example grep searches the output of `systemctl list-units --type=service` for lines with `running` in them and returns only the lines matching the pattern.

From our command above and you will notice a couple of services that we are using already, the `ssh.service` is what is running in the background to allow SSH to operate. **You'll also see two things we have installed, docker and postgres, which both run in the background as services!**

If you had a lot more services and it was hard to see what was running. You could also use `grep` to check whether postgres was there for example!

<br>

# 2️⃣ Creating a script

❓ Let's start by creating a `check_ssh.sh` script which checks whether any users are currently connected by SSH, `echo` if there are users connected and otherwise `poweroff` the VM!

📚 Some things worth exploring in relation to the script if you are not familiar with bash scripts:
- Start with `#!/usr/bin/env bash`. This is commonly called a [shebang](https://en.wikipedia.org/wiki/Shebang_(Unix)). It tells your computer that this file should be run using `bash`. Specifically the `bash` executable for the user that executes the script.
- Go back to the lecture and check the control flow syntax there!
- Use `ss | grep "tcp.*ssh"` to check for SSH users

<details>
<summary markdown='span'>🎁 Solution</summary>

```bash
#!/usr/bin/env bash
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

❗️ **The command we just used, `chmod`, can do more than just make a file executable**. It also affects who can read, write, and execute files! Bookmark this [great article 🔗](https://www.computerhope.com/unix/uchmod.htm) for later if you want to learn a bit more about this concept.
<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W1D5/010102-file-permissions-and-ownership-in-linux.png" width=400>

❓ Lets move our script into `/usr/local` before we move on.

You might notice you get permission denied when trying to move the files into the folder you can fix this with sudo (💡 a useful trick if you forget a sudo is running `sudo !!`. This command runs the previous command but with `sudo` prepended). You need this because only the root user can edit the root directory (along with everything on the system). Running `sudo` allows you to imitate the root user to run one command (a more in-depth look at [root](http://www.linfo.org/root.html)). This control over absolutely everything on the system is one of the most powerful things about linux. But you also must be careful not to overwrite key files, there is a lack of guard rails.

<details>
  <summary markdown='span'>💡 Why /usr/local</summary>

If you want a quick explanation of most of the folders in the root directory (i.e. the highest folder in the system) this 3 min video explains the [linux filesystem](https://www.youtube.com/watch?v=42iQKuQodW4) at a high level.
</details>

<br>

# 3️⃣ Automation with cronjobs

Cron is a way of running commands at a **specific time** of day. Cron is good for running short scripts at a particular time. If you wanted to run more complex, long running processes or a process that has to be executed very often, automating with a linux service could be more appropriate, but that's a bit out of scope for what we're doing here.

Let's open the **crontab** that keeps track of cron jobs:

```bash
sudo crontab -e
```

The syntax for cron can be a little strange at first, to run `echo` once a day at 10pm you would write:

```bash
0 22 * * * echo "I'm going to be printed every day at 10pm"
```

The general format is:
- 5 values separated by a whitespace, each value denote a time period:
    - The first is minutes (0 - 59)
    - Hour (0 - 23)
    - Day of the Month (1 - 31)
    - Month (1 - 12)
    - Day of the Week (Sunday, Monday, Tuesday, etc..) (0 - 6. 0 is Sunday)
- The following section (`echo "I'm going to be printed every day at 10pm"`) is the program that you want to execute plus any arguments.

A `*` character means that cron will run for every time period for that value. A way to interpret `0 22 * * *` would be: At the zero'th minute of the 22nd hour, of every day, of every month, of every day of the week.

There are also some additional operators that work with cron syntax, some useful ones are:
- `,` value list separator
- `-` range of values
- `/` step values

For example, if I wanted to execute a command at 12:00 (midday) and 00:00 (midnight), the syntax could be either of:

```bash
0 0,12 * * * echo "I'm going to be printed every 12 hours"

0 */12 * * * echo "I'm also going to be printed every 12 hours"
```

The [website at this link here 🔗](https://crontab.guru/#0_20_*_*_*) is great for checking your syntax!

❓ In **crontab** you should add a line to execute your shell script on a schedule! A good time period is **every 15 minutes**. Remember that your shell script is not a binary, so you will need the full path.

❗ Make sure that your script is not being run too often! It takes some time for your VM to turn on. If your shell script is running every minute, then the script might turn off your VM before you can connect and you will lock yourself out of your VM!

<details>
  <summary markdown='span'>🎁 crontab solution</summary>

```bash
*/15 * * * * /usr/local/check_ssh.sh
```
</details>

<br>

# 🏁 Finishing up

Cron and crontab if a simple but powerful tool in the linux arsenal. Here we have set a small fail safe that will automatically turn off our VM if we forget, but you could also use it for some basic orchestration!

🏁 We now have a cron which starts a timer running on our to check if anyone is connected and if not shut it down, stopping us spending too much money by accidentally leaving it on overnight!

<br>
