#!/usr/bin/env python3.7

import argparse
import os
import sys
import jsonlines

from metrics.running_average import running_average


def valid_input_file(f):
    """
    Checks if a given file path leads to a valid file or to STDIN.
    In case a file path is passed, we will check if it is valid and readable and return it.
    In case '-' is passed, we will return STDIN.
    If a file path is passed, remember to close the file descriptor after you are done with it.

    :param f: the file path to check, or '-' for STDIN.
    :return: a file stream (opened file) that can be either for a file or STDIN
    """
    if f == '-':
        return sys.stdin
    else:
        # a valid input file is a file that exists and is readable
        if not (os.path.isfile(f) and os.access(f, os.R_OK)):
            raise argparse.ArgumentTypeError("Cannot access this file! Are you sure it exists \
            and you have read permission?")
        else:
            return open(f)


def do_main():
    """
    Will parse arguments and start all the metrics calculations.
    """
    parser = argparse.ArgumentParser(description='Unbabel translation metrics stream parsing CLI.')
    parser.add_argument('--input_file', type=valid_input_file, required=True,
                        help='the JSON file containing the data related to the translations to process \
                        or - if you want the tool to read directly from the standard input.')
    parser.add_argument('--window_size', type=int, required=True,
                        help='the window size (in minutes) for the translations to average.')
    args = parser.parse_args()

    # use jsonlines to create a stream of JSON objects from a text stream
    json_stream = jsonlines.Reader(args.input_file)

    # metrics calculations here, we're only doing running averages for now
    running_average(json_stream, args.window_size)

    # If we have a file opened that is not stdin, we should close it
    if args.input_file is not sys.stdin:
        args.input_file.close()


if __name__ == "__main__":
    do_main()
