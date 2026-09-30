#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
Generate an ascii bar chart for input data

https://github.com/bitly/data_hacks
"""
import sys
import math
import shutil
from collections import defaultdict
from optparse import OptionParser
from decimal import Decimal

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
            if not clean_line:
                print("invalid line %r" % line, file=sys.stderr)
                continue
        if clean_line[0] in ['"', "'"]:
            clean_line = clean_line.strip('"').strip("'")
        if clean_line:
            yield clean_line

def run(input_stream, options):
    data = defaultdict(int)
    total = 0
    for row in input_stream:
        if options.agg_key_value:
            kv = row.rstrip().rsplit(None, 1)
            value = int(kv[1])
            data[kv[0]] += value
            total += value
        elif options.agg_value_key:
            kv = row.lstrip().split(None, 1)
            value = int(kv[0])
            data[kv[1]] += value
            total += value
        else:
            data[row] += 1
            total += 1
    
    if not data:
        print("Error: no data")
        sys.exit(1)
    
    max_length = max([len(key) for key in list(data.keys())])
    max_length = min(max_length, 50)
    # key, " [%6d] " and the optional percentage surround the bar
    value_characters = options.width - max_length - len(" [000000] ")
    if options.percentage:
        value_characters -= len(" (100.00%)")
    value_characters = max(10, value_characters)
    max_value = max(data.values())
    scale = int(math.ceil(float(max_value) / value_characters))
    scale = max(1, scale)
    
    print(("# each " + options.dot + " represents a count of %d. total %d" % (scale, total)))
    
    if options.sort_values:
        data = [[value, key] for key, value in list(data.items())]
        data.sort(key=lambda x: x[0], reverse=options.reverse_sort)
    else:
        # sort by keys
        data = [[value, key] for key, value in list(data.items())]
        if options.numeric_sort:
            # keys could be numeric too
            data.sort(key=lambda x: (Decimal(x[1])), reverse=options.reverse_sort)
        else:
            data.sort(key=lambda x: x[1], reverse=options.reverse_sort)
    
    str_format = "%" + str(max_length) + "s [%6d] %s%s"
    percentage = ""
    for value, key in data:
        if options.percentage:
            percentage = " (%0.2f%%)" % (100 * Decimal(value) / Decimal(total))
        print((str_format % (key[:max_length], value, int(value / scale) * options.dot, percentage)))

def main():
    parser = OptionParser()
    parser.usage = "cat data | %prog [options]"
    parser.add_option("-a", "--agg", dest="agg_value_key", default=False, action="store_true",
                        help="Two column input format, space seperated with value<space>key")
    parser.add_option("-A", "--agg-key-value", dest="agg_key_value", default=False, action="store_true",
                        help="Two column input format, space seperated with key<space>value")
    parser.add_option("-k", "--sort-keys", dest="sort_keys", default=True, action="store_true",
                        help="sort by the key [default]")
    parser.add_option("-v", "--sort-values", dest="sort_values", default=False, action="store_true",
                        help="sort by the frequence")
    parser.add_option("-r", "--reverse-sort", dest="reverse_sort", default=False, action="store_true",
                        help="reverse the sort")
    parser.add_option("-n", "--numeric-sort", dest="numeric_sort", default=False, action="store_true",
                        help="sort keys by numeric sequencing")
    parser.add_option("-p", "--percentage", dest="percentage", default=False, action="store_true",
                        help="List percentage for each bar")
    parser.add_option("--dot", dest="dot", default='∎', help="Dot representation")
    parser.add_option("-w", "--width", dest="width", type="int",
                      default=shutil.get_terminal_size().columns,
                      help="Output width in characters [default: terminal width, or 80 when piped]")
    parser.add_option("-c", "--column", dest="field", type="int",
                      help="Use only this column of each line (1-based, negative counts from the end)")
    parser.add_option("-d", "--delimiter", dest="delimiter",
                      help="Column delimiter for --column [default: whitespace]")

    (options, args) = parser.parse_args()
    if options.field == 0:
        parser.error("--column is 1-based; use -1 for the last column")
    if options.field and (options.agg_value_key or options.agg_key_value):
        parser.error("--column cannot be combined with -a/-A")
    
    if sys.stdin.isatty():
        parser.print_usage()
        print("for more help use --help")
        sys.exit(1)
    run(load_stream(sys.stdin, options.field, options.delimiter), options)

if __name__ == "__main__":
    main()

