#!/usr/bin/env python3.6

import sys
import datetime
import json

# template object for a translation_delivered event
template = {
        'timestamp': None,
        'translation_id': None,
        'nr_words': None,
        'duration': None,
        'source_language': 'en',
        'target_language': 'fr',
        'client_name': 'easyjet',
        'event_name': 'translation_delivered',
}

def do_main():
    max_translations = int(sys.argv[1])
    minutes_multiplier = float(sys.argv[2])

    tid = 0
    while tid < max_translations:
        # fill the template and print it out
        template['translation_id'] = tid
        template['timestamp'] = (datetime.datetime.now() + datetime.timedelta(minutes=(tid*minutes_multiplier)))\
                .strftime("%Y-%m-%d %H:%M:%S.%f")
        template['nr_words'] = (tid * 8) % 350
        template['duration'] = (tid * 8) % 350

        print(json.dumps(template))
        tid += 1

if __name__ == '__main__':
    do_main()
