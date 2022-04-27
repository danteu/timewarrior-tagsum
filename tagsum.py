#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
timewarrior-tagsum
Print the sum of time spent on each of the selected tags in the
selected time frame.

Usage:
timew report tagsum [range] [tag]
timew tagsum [range] [tag]
"""

from datetime import datetime, timedelta
import json
from sys import stdin

DATETIME_FORMAT = "%Y%m%dT%H%M%SZ"


def print_tags(i_dict: dict) -> None:
    """
    Prints all tags and the time spent on them, as well as the total
    sum of time spent on all tags.
    """
    if not i_dict:
        return

    total_time = sum(i_dict.values(), timedelta())

    maxlen_key = max(
        len(max(i_dict, key=lambda k: len(k))),
        len('Total')
    )
    maxlen_time = max(
        len(str(i_dict[max(i_dict, key=lambda k: len(str(i_dict[k])))])),
        len(str(total_time))
    )

    for key in sorted(i_dict):
        print(key.ljust(maxlen_key), '--',
              str(i_dict[key]).rjust(maxlen_time))

    print('')
    print('Total'.ljust(maxlen_key), '--', f'{total_time}'.rjust(maxlen_time))


def interval_len(start, end: str) -> timedelta:
    """
    Returns the length of the time interval between start and end.
    If end is None, i.e, the passed interval is open, returns the time
    between start and now.
    """
    start_date = datetime.strptime(start, DATETIME_FORMAT)
    end_date = (datetime.utcnow()
                if end is None
                else datetime.strptime(end, DATETIME_FORMAT))

    i_len = end_date - start_date
    i_len -= timedelta(microseconds=i_len.microseconds)
    return i_len


def sum_tags(data) -> dict[str, timedelta]:
    """
    Returns a dict that contains the total time spent on each tag in body.
    """
    i_dict = {}
    for x in data:
        tags = x.get("tags") if ("tags" in x) else ["__untagged"]
        for t in tags:
            mylen = interval_len(x.get("start"), x.get("end"))
            if t not in i_dict:
                i_dict[t] = timedelta(0)
            i_dict[t] = i_dict[t] + mylen
    return i_dict


def main() -> None:
    """
    Reads the config options and the JSON data from stdin, parses the JSON
    data and prints the tags and the tracked time.
    """
    for line in stdin:
        if line == "\n":
            break

    data = ''
    for line in stdin:
        data += line

    data_parsed = json.loads(data)
    print_tags(sum_tags(data_parsed))


if __name__ == "__main__":
    main()
