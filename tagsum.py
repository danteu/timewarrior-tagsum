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

from datetime import datetime, timedelta, UTC, timezone
import json
from sys import stdin

DATETIME_FORMAT = "%Y%m%dT%H%M%SZ"


def print_tags(i_tuple: tuple[timedelta, dict[str, timedelta]]) -> None:
    """
    Prints all tags and the time spent on them, as well as the total
    sum of time spent on all tags.
    """
    if not i_tuple:
        return

    i_dict = i_tuple[1]
    total_time = i_tuple[0]

    maxlen_key = max(
        len(max(i_dict, key=len)),
        len('Total')
    )
    maxlen_time = max(
        len(str(i_dict[max(i_dict, key=lambda k: len(str(i_dict[k])))])),
        len(str(total_time))
    )

    for key in sorted(i_dict):
        print(key.ljust(maxlen_key), '--', str(i_dict[key]).rjust(maxlen_time))

    print('')
    print('Total'.ljust(maxlen_key), '--', f'{total_time}'.rjust(maxlen_time))


def interval_len(start: datetime, end: datetime) -> timedelta:
    """
    Returns the length of the time interval between start and end.
    """
    i_len = end - start
    i_len -= timedelta(microseconds=i_len.microseconds)
    return i_len


def sum_tags(
    data: list[dict[str, datetime]]
) -> tuple[timedelta, dict[str, timedelta]]:
    """
    Returns a dict that contains the total time spent on each tag in body.
    """
    i_dict = {}
    total_time = timedelta(0)
    for entry in data:
        tags = entry.get("tags") if ("tags" in entry) else ["__untagged"]
        i_len = interval_len(entry.get("start"), entry.get("end"))
        total_time += i_len

        for tag in tags:
            if tag not in i_dict:
                i_dict[tag] = timedelta(0)
            i_dict[tag] = i_dict[tag] + i_len
    return (total_time, i_dict)


def convert_timestamps(data: list[dict[str, str]], rep_start: str, rep_end: str) -> None:
    """
    Converts the start and end dates in the `data` list to datetime. Makes sure
    that no date lies outside of the (`rep_start`, `rep_end`) interval. If an
    interval is open, i.e., there is an open time recording, sets the end time to now.
    """
    rep_start = (
        datetime.min.replace(tzinfo=timezone.utc)
        if rep_start is None
        else datetime.strptime(rep_start.strip(), DATETIME_FORMAT).replace(
            tzinfo=timezone.utc
        )
    )

    rep_end = (
        datetime.max.replace(tzinfo=timezone.utc)
        if rep_end is None
        else datetime.strptime(rep_end.strip(), DATETIME_FORMAT).replace(
            tzinfo=timezone.utc
        )
    )

    for entry in data:
        entry["start"] = max(
            datetime.strptime(entry["start"], DATETIME_FORMAT).replace(
                tzinfo=timezone.utc
            ),
            rep_start
        )
        entry["end"] = (
            datetime.now(UTC)
            if entry.get("end") is None
            else min(
                datetime.strptime(entry["end"], DATETIME_FORMAT).replace(
                    tzinfo=timezone.utc
                ),
                rep_end,
            )
        )


def main() -> None:
    """
    Reads the config options and the JSON data from stdin, parses the JSON
    data and prints the tags and the tracked time.
    """
    for line in stdin:
        if line == "\n":
            break
        key, *values = line.split(': ', 1)
        if key == 'temp.report.start':
            report_start = values[0].strip()
        elif key == 'temp.report.end':
            report_end = values[0].strip()

    data = json.load(stdin)
    convert_timestamps(data, report_start or None, report_end or None)
    print_tags(sum_tags(data))


if __name__ == "__main__":
    main()
