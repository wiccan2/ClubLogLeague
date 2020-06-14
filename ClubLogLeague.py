#! /bin/env python

# Copyright © 2020 Antony Jordan <antony.r.jordan@gmail.com>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.


# ###########################################################################################################################
# Imported Libraries
# ###########################################################################################################################

import argparse
import csv
import json
import urllib.request
from enum import Enum
from typing import Optional, List


# ###########################################################################################################################
# External Code
# ###########################################################################################################################

class ArgTypeMixin(Enum):
    """
    Lovingly stolen from: https://gist.github.com/ptmcg/23ba6e42d51711da44ba1216c53af4ea
    """

    @classmethod
    def argtype(cls, s: str) -> Enum:
        try:
            return cls[s]
        except KeyError:
            raise argparse.ArgumentTypeError(
                f"{s!r} is not a valid {cls.__name__}")

    def __str__(self):
        return self.name


# ###########################################################################################################################
# Enumerations
# ###########################################################################################################################

class Mode(ArgTypeMixin, Enum):
    All = 0
    CW = 1
    Phone = 2
    Data = 3


class QSL(ArgTypeMixin, Enum):
    Worked = 0
    Confirmed = 1


class Date(ArgTypeMixin, Enum):
    """
    0 = No date filter
    1 = The last 12 months (eg. if today is 12 June 2016, then the range is 12 June 2015 to 12 June 2016)
    2 = Not used
    3 = This year (e.g. if today is between 1 January and 31 December 2016, then the year is 2016)
    4 = Last year (e.g. if today is between 1 January and 31 December 2016, then last year is 2015)
    """
    All = 0
    Past12 = 1
    CurrentYear = 3
    LastYear = 4


class Deleted(ArgTypeMixin, Enum):
    Current = 0
    All = 1


# ###########################################################################################################################
# Data gathering/processiong
# ###########################################################################################################################

def request_league(
        mode: Mode = Mode.All,
        qsl: QSL = QSL.Worked,
        date: Date = Date.All,
        club: int = 0,
        deleted: Deleted = Deleted.Current
) -> []:
    # Form the URL for the API call
    # See: https://clublog.freshdesk.com/support/solutions/articles/3000054404-downloading-dxcc-leagues-as-json
    arguments = f'mode={mode.value}&qsl={qsl.value}&date={date.value}&club={club}&deleted={deleted.value}'
    url = f'https://clublog.org/league_api.php?{arguments}'

    print(f'URL={url}')

    # Request the data from the server
    response = urllib.request.urlopen(url, timeout=15)

    # Ensure that the request was successful
    if response.code == 200:
        # Grab the actual data from the server's response
        raw_data = response.read().decode()

        # The server seems to provide invalid JSON data so lets fix it by adding the required list delimiters.
        fixed_data = f"[{raw_data.replace('][', '],[')}]"

        # Return the data parsed into a Python list.
        return json.loads(fixed_data)

    # If we weren't successful print out the error from the server.
    print(f'Error: {response.code} - {response.msg}')

    # If we weren't successful in our request return an error value.
    return None


def process_league(data: List, exclude: Optional[List] = None) -> List:
    # If the exclude parameter has not been passed create an empty list for it.
    if exclude is None:
        exclude = []

    # The empty list to be populate with league data.
    league = []

    # Set the initial value for the last rank variable.
    # This is used to recalculate the rank if a call has been skipped.
    last_rank = 1

    # Loop over each entry in the raw data
    for data_entry in data:
        rank = int(data_entry[0])
        call = data_entry[1]

        # If the call is in the list of excludes move onto the next one
        if call in exclude:
            continue

        # If the rank has gotten out of sequence due to an excluded call, recalculate it.
        if rank > (last_rank + 1):
            rank = last_rank + 1

        # Set the last_rank so that we can calculate a new one if needed for the next call
        last_rank = rank

        # Append the data for this call to the league with some headers to make it readable.
        league.append({
            'Rank': rank,
            'Call': call,
            'DXCCs': data_entry[2],
            'Slots': data_entry[3],
            '160M': data_entry[4]['160'],
            '80M': data_entry[4]['80'],
            '60M': data_entry[4]['60'],
            '40M': data_entry[4]['40'],
            '30M': data_entry[4]['30'],
            '20M': data_entry[4]['20'],
            '17M': data_entry[4]['17'],
            '15M': data_entry[4]['15'],
            '12M': data_entry[4]['12'],
            '10M': data_entry[4]['10'],
            '6M': data_entry[4]['6'],
            '4M': data_entry[4]['4'],
            '2M': data_entry[4]['2'],
            '70CM': data_entry[4]['70'],
            '23CM': data_entry[4]['23'],
            '13CM': data_entry[4]['13'],
        })

    # Return the processed league
    return league


def write_csv(league: [], csv_path: str = './league.csv'):
    # Check that we actually have some data to write
    if len(league) < 1:
        # Raise an error if we don't.
        raise RuntimeError('The league is empty.')

    # Open the specified CSV file for writing
    with open(csv_path, 'w', newline='') as csv_file:
        # Create a CSV writer object.
        # The field names are the keys from the league data.
        writer = csv.DictWriter(csv_file, fieldnames=league[0].keys())

        # Write the header row to the CSV file.
        writer.writeheader()

        # Loop over each league entry.
        for entry in league:
            # Write the entry as a row in the CSV file.
            writer.writerow(entry)


# ###########################################################################################################################
# User interface
# ###########################################################################################################################

def create_cli():
    parser = argparse.ArgumentParser(description='Request DXCC league table from ClubLog.org')

    parser.add_argument('-o', '--csv_file', metavar='PATH', type=str, default='./league.csv',
                        help='the path to write the CSV file to (defaults to `./league.csv`')

    # noinspection PyTypeChecker
    parser.add_argument('-m', '--mode', type=Mode.argtype, choices=Mode, default=Mode.All, help='filter by mode')
    # noinspection PyTypeChecker
    parser.add_argument('-q', '--qsl', type=QSL.argtype, choices=QSL, default=QSL.Worked,
                        help='filter by worked or confirmed status')
    # noinspection PyTypeChecker
    parser.add_argument('-d', '--date', type=Date.argtype, choices=Date, default=Date.All, help='filter by date')
    parser.add_argument('-c', '--club', type=int, default=0, metavar='ID',
                        help='filter by club, defaults to global list.'
                             'Must be the ID number for the desired club.'
                             'See https://tinyurl.com/ybs9zx7n for details of how to obtain the ID.')
    # noinspection PyTypeChecker
    parser.add_argument('-D', '--deleted', type=Deleted.argtype, choices=Deleted, default=Deleted.Current,
                        help='filter by inclusion of deleted entries')
    parser.add_argument('-e', '--exclude', metavar='CALL', type=str, nargs='+', default=[],
                        help='removes the specified calls from the results')

    return parser


def _main(mode: Mode, qsl: QSL, date: Date, club: int, deleted: Deleted, exclude: List, csv_path: str):
    data = request_league(mode=mode, qsl=qsl, date=date, club=club, deleted=deleted)
    league = process_league(data, exclude=exclude)
    write_csv(league, csv_path=csv_path)


# ###########################################################################################################################
# The main entry point for the script
# ###########################################################################################################################

if __name__ == '__main__':
    ARGS = create_cli().parse_args()
    print(ARGS)
    _main(ARGS.mode, ARGS.qsl, ARGS.date, ARGS.club, ARGS.deleted, ARGS.exclude, ARGS.csv_file)
