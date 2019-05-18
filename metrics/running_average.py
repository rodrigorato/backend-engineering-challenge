from collections import deque
import datetime
import json


def is_translation_delivered_event(e):
    """
    Find if any given event is a 'translation_delivered' event.

    :param e: the event
    :return: True if it is a 'translation_delivered' event, False otheriwse
    """
    return e.get('event_name') == 'translation_delivered'


def print_running_average_json(date, avg):
    """
    Print out a running average as a JSON object.

    :param date: the date as a datetime object for the average's timestamp
    :param avg: the average to print
    """
    date_str = date.strftime('%Y-%m-%d %H:%M:%S')
    print(json.dumps({'date': date_str, 'average_delivery_time': avg}))


def parse_timestamp_into_datetime(ts):
    """
    Parses a timestamp as a date string in the Y-m-d H-M-S.f format into a datetime object

    :param ts: the timestamp string
    :return: a datetime object representing ts
    """
    return datetime.datetime.strptime(ts, '%Y-%m-%d %H:%M:%S.%f')


def running_average(json_stream, window_size):
    """
    Calculates and outputs (prints) a running average using the data in json_stream.
    The averages will be calculated minute by minute using the elements from the last window_size minutes.

    :param json_stream: a stream of JSON objects where 'translation_delivered' events can be found
    :param window_size: the window_size in minutes, as an integer, for the translations we're interested in each average
    """
    # we'll be running the elements in the current window through a deque, and count their average
    deq = deque()
    deq_avg = 0
    window_ts = None  # we also keep a timestamp for the end of the current window

    # filter our stream of data, as we only care about 'translation_delivered' events
    delivery_stream = filter(is_translation_delivered_event, json_stream)

    first = True  # we want to know if it is the first translation to show a blank average
    for del_evt in delivery_stream:

        # parse the current event's timestamp into a datetime object
        del_ts = parse_timestamp_into_datetime(del_evt['timestamp'])

        if first:
            # if we're looking at the first translation, our window ends at its minute
            window_ts = datetime.datetime(del_ts.year, del_ts.month, del_ts.day, del_ts.hour, del_ts.minute, 0)

            first = False
            print_running_average_json(window_ts, deq_avg)  # just show a 0 average

            window_ts += datetime.timedelta(minutes=1)

        else:
            # advance our window minute by minute until the event is in the window
            while window_ts < del_ts:

                # but remove elements older than window_size minutes first
                while deq and parse_timestamp_into_datetime(deq[0]['timestamp']) < (window_ts - datetime.timedelta(minutes=window_size)):
                    evt = deq.popleft()

                    # lookout when removing the last event from the deque
                    if deq:
                        deq_avg -= (evt['duration'] - deq_avg)/len(deq)
                    else:
                        deq_avg = 0

                print_running_average_json(window_ts, deq_avg)
                window_ts += datetime.timedelta(minutes=1)

        # Add the new event and add it to the average
        deq.append(del_evt)
        deq_avg += (del_evt['duration'] - deq_avg)/len(deq)

    print_running_average_json(window_ts, deq_avg)
