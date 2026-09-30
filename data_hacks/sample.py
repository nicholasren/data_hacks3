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
Pass through a sampled percentage of data

https://github.com/bitly/data_hacks
"""

import sys
import random
from optparse import OptionParser
from decimal import Decimal, InvalidOperation

def run(sample_rate):
    input_stream = sys.stdin
    threshold = float(sample_rate) / 100
    for line in input_stream:
        if random.random() < threshold:
            sys.stdout.write(line)

def get_sample_rate(rate_string):
    """ return a rate as a percentage"""
    try:
        if rate_string.endswith("%"):
            rate = Decimal(rate_string[:-1])
        elif '/' in rate_string:
            x, y  = rate_string.split('/')
            rate = Decimal(x) / Decimal(y) * 100
        else:
            raise ValueError
    except (ValueError, InvalidOperation, ArithmeticError):
        raise ValueError("rate %r is invalid rate format must be '10%%', '0.1%%' or '1/10'" % rate_string)
    if rate <= 0 or rate > 100:
        raise ValueError('rate %r must be 0%% < rate <= 100%% ' % rate_string)
    return rate

def main():
    parser = OptionParser(usage="cat data | %prog [options] [sample_rate]")
    parser.add_option("--verbose", dest="verbose", default=False, action="store_true")
    parser.add_option("--seed", dest="seed", type="int",
                      help="Random seed, for a reproducible sample")
    (options, args) = parser.parse_args()
    
    if not args or sys.stdin.isatty():
        parser.print_usage()
        sys.exit(1)
    
    try:
        sample_rate = get_sample_rate(args[-1])
    except ValueError as e:
        print(e, file=sys.stderr)
        parser.print_usage()
        sys.exit(1)
    if options.verbose:
        print("Sample rate is %s%%" % sample_rate, file=sys.stderr) 
    if options.seed is not None:
        random.seed(options.seed)
    run(sample_rate)

if __name__ == "__main__":
    main()
