#!/usr/bin/env python3.6

import argparse
import os
import sys

def valid_input_file(f):
    """Checks if a given file path leads to a valid file or stdin.
    In case a file path is passed, will check if it is a valid file and is readable.
    In case '-' is passed, will use stdin.
    """

    if f == '-':
        return sys.stdin
    else:
        if not (os.path.isfile(f) and os.access(f, os.R_OK)):  # a valid input file is a file that exists and is readable
            raise argparse.ArgumentTypeError("Cannot access this file! Are you sure it exists and you have read permission?")
        else:
            return open(f)

def do_main():
    parser = argparse.ArgumentParser(description='Unbabel translation metrics stream parsing CLI.')
    parser.add_argument('--input_file', type=valid_input_file, required=True,
                        help='the JSON file containing the data related to the translations to process.')
    parser.add_argument('--window_size', type=int, required=True,
                        help='the window size (in minutes) for the translations to average.')

    args = parser.parse_args()


    # If we have a file opened that is not stdin, we should close it
    if args.input_file is not sys.stdin:
        args.input_file.close()

if __name__ == "__main__":
    do_main()
