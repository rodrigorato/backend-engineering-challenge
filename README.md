# Backend Engineering Challenge
Hello, welcome to my solution for this challenge.

One tiny note before I start explaining my solution: the original challenge is [right here](CHALL.md), and you should read it in order to understand what I'll explain next.

## Solution and Architecture
### Foreword
The problem we're being asked to solve is a combination of two different problems.

There is the problem of calculating a **running average**, which wouldn't be a problem at all if we could store all the data in memory, but isn't the case here (as I explain below).
The solution to this problem is rather easy, and it consists in simply keeping an average value and a count of how many items are being used in that average.

The other problem is a typical **sliding window problem**, which can usually be solved in _O(n)_ by using a Queue.
This task combines both these problems, which means that the **running average** will have to decrease eventually, which is a tiny variation on the usual algorithm.

A _Complexity Analysis_ of this solution is also provided below.

### Key Ideas
This program has been developed around the concept that its input will come **in real-time** from a stream of data, possibly bigger than the ammount of memory available for the program to run.
In this sense, we cannot solve this problem by storing all the data that we want to process.
We can, however, rely on the fact that the events that are being fed into the program are ordered chronologically by their timestamp, as they are being produced and fed to the program **in real-time**.

To solve this, the program is built around streams, meaning that it should always be processing data and outputing its results in real-time as well.
To achieve this, the program can take its input from a regular file (which in an Unix system can even be a network socket, for example), or from its standard input (`stdin`).
This way, the program can be used in statistics pipelines, composed with with other utilities, and eventually the tool that is producing its input.
It will, in no way shape or form, stop this pipeline to process data, as it will process and output data as soon as possible.

### Architecture
 TODO


## Installing and Running
### Prerequisites
This project was developed for `Python 3.7`, and uses the PyPI packages in the `requirements.txt` file.
Before trying to run this code, you should install the packages.

Here is how you can install these packages using Pip:
```bash
pip3 install -r requirements.txt
```

Once you do this, you're all good to run the code! :)

### Running the Project
If you're running this in a Unix/Linux system, where you have a `/usr/bin/env` that knows about `python3.6`, you can just set the `metrics_cli.py` script as executable and run it, like so:
```bash
chmod u+x metrics_cli.py
./metrics_cli.py <arguments>
```

If you did not understand what I meant with `/usr/bin/env` or just want to be a little more conservative, you can run the project like so:
```bash
/path/to/python3.7 metrics_cli.py <arguments>
```

In both of these cases, I denoted the program arguments with `<arguments>`.
You can check what are the valid arguments by running the program with no arguments, or with the `-h` flag.
In any case, both the `--input_file` and `--window_size` arguments specified in the [original challenge description](CHALL.md) are required.

### Usage
The CLI application has two arguments that are mandatory-
#### input\_file
The `--input_file` is an argument that tells the program where to get a stream of JSON object from.
This stream is what will be used and processed in order to produce the running average of the translations' durations.

There are two types of arguments you can pass here, you can specify a path to a valid file (like `./path/to/events.json`), or you can pass a special value, `-`, that tells the program to read from its standard input (much like standard Unix utilities, such as `cat`).

Nonetheless, the program will read from that stream until it ends/finds an `EOF`.

#### window\_size
The `--window_size` argument represents how many minutes the program will use a translation for a running average.
For example, if you pass `--window_size 10`, only translations that occurred in the last 10 minutes will be used for the current running average.


## Complexity Analysis
 TODO
