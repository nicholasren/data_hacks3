#!/usr/bin/env python
#
# Copyright 2010 Bitly
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""
Calculate percentiles (95% by default) from a list of values given on stdin

https://github.com/bitly/data_hacks
"""

import sys
from decimal import Decimal, InvalidOperation
from optparse import OptionParser


def select_field(line, field, delimiter):
    """return the 1-based field of line (negative counts from the end), or
    None when the line has no such field"""
    parts = line.split(delimiter)
    try:
        return parts[field - 1 if field > 0 else field].strip()
    except IndexError:
        return None


def load_stream(input_stream, field=None, delimiter=None):
    for line in input_stream:
        clean_line = line.strip()
        if not clean_line:
            # skip empty lines (ie: newlines)
            continue
        if field:
            clean_line = select_field(clean_line, field, delimiter)
        try:
            yield Decimal(clean_line)
        except (InvalidOperation, TypeError):
            print("invalid line %r" % line, file=sys.stderr)


def calc_percentile(data, count, percentile):
    """find the value at the given percentile, where data maps value -> number
    of occurrences and count is the total number of occurrences"""
    threshold = Decimal(count) * percentile / 100
    seen = 0
    for value in sorted(data):
        # increment our count by the # of items with this value
        seen += data[value]
        if seen > threshold:
            return value
    # the 100th percentile is the maximum
    return max(data)


def parse_percentiles(percentiles_string):
    percentiles = []
    for p in percentiles_string.split(','):
        try:
            percentile = Decimal(p.strip().rstrip('%'))
        except InvalidOperation:
            raise ValueError("invalid percentile %r" % p)
        if not 0 < percentile <= 100:
            raise ValueError("percentile %r must be 0 < p <= 100" % p)
        percentiles.append(percentile)
    return percentiles


def run(input_stream, options):
    data = {}
    count = 0
    total = Decimal(0)
    for value in input_stream:
        data[value] = data.get(value, 0) + 1
        count += 1
        total += value

    if not data:
        print("Error: no data", file=sys.stderr)
        sys.exit(1)

    if len(options.percentiles) == 1 and not options.summary:
        print(calc_percentile(data, count, options.percentiles[0]))
        return

    if options.summary:
        print("count\t%d" % count)
        print("min\t%s" % min(data))
        print("max\t%s" % max(data))
        print("mean\t%s" % (total / count))
    for percentile in options.percentiles:
        print("p%s\t%s" % (percentile, calc_percentile(data, count, percentile)))


def main():
    parser = OptionParser()
    parser.usage = "cat data | %prog [options]"
    parser.add_option("-p", "--percentiles", dest="percentiles", default="95",
                      help="Comma separated list of percentiles to " +
                      "calculate [default: 95]")
    parser.add_option("-s", "--summary", dest="summary", default=False,
                      action="store_true",
                      help="Also print count, min, max and mean")
    parser.add_option("-c", "--column", dest="field", type="int",
                      help="Use only this column of each line (1-based, " +
                      "negative counts from the end)")
    parser.add_option("-d", "--delimiter", dest="delimiter",
                      help="Column delimiter for --column [default: whitespace]")

    (options, args) = parser.parse_args()
    if options.field == 0:
        parser.error("--column is 1-based; use -1 for the last column")
    try:
        options.percentiles = parse_percentiles(options.percentiles)
    except ValueError as e:
        parser.error(str(e))

    if sys.stdin.isatty():
        parser.print_usage()
        print("for more help use --help")
        sys.exit(1)
    run(load_stream(sys.stdin, options.field, options.delimiter), options)


if __name__ == "__main__":
    main()
