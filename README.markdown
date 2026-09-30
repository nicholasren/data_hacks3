data_hacks3
==========
Command line utilities for data analysis.
This is a python3 port of [data_hacks](https://github.com/bitly/data_hacks).


Installing: `pip install data_hacks3`

data_hacks3 are friendly. Ask them for usage information with `--help`

Each tool is installed under its plain name (`histogram`, `bar_chart`, `percentile`,
`ninety_five_percent`, `sample`, `run_for`) and under its original `*.py` name.

`histogram.py`, `bar_chart.py` and `percentile.py` can pick one column out of each
line with `-c/--column N` (1-based; `-c -1` is the last column) and `-d/--delimiter`
(whitespace by default), so there's no need for `awk '{print $NF}' |` in front.
`histogram.py` and `bar_chart.py` size their bars to the terminal width; override it
with `-w/--width`.

histogram.py
------------

A utility that parses input data points and outputs a text histogram

Example:

    $ cat /tmp/data | histogram.py --percentage --max=1000 --min=0
    # NumSamples = 60; Min = 0.00; Max = 1000.00
    # 1 value outside of min/max
    # Mean = 332.666667; Variance = 471056.055556; SD = 686.335236; Median 191.000000
    # each ∎ represents a count of 1
        0.0000 -   100.0000 [    28]: ∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎ (46.67%)
      100.0000 -   200.0000 [     2]: ∎∎ (3.33%)
      200.0000 -   300.0000 [     2]: ∎∎ (3.33%)
      300.0000 -   400.0000 [     8]: ∎∎∎∎∎∎∎∎ (13.33%)
      400.0000 -   500.0000 [     8]: ∎∎∎∎∎∎∎∎ (13.33%)
      500.0000 -   600.0000 [     7]: ∎∎∎∎∎∎∎ (11.67%)
      600.0000 -   700.0000 [     3]: ∎∎∎ (5.00%)
      700.0000 -   800.0000 [     0]:  (0.00%)
      800.0000 -   900.0000 [     1]: ∎ (1.67%)
      900.0000 -  1000.0000 [     0]:  (0.00%)

With logarithmic scale

    $ printf 'import random\nfor i in range(1000):\n print random.randint(0,10000)'|\
        python -|./data_hacks/histogram.py -l
    # NumSamples = 1000; Min = 2.00; Max = 9993.00
    # Mean = 4951.757000; Variance = 8279390.995951; SD = 2877.393090; Median 4828.000000
    # each ∎ represents a count of 6
        2.0000 -    11.7664 [     3]:
       11.7664 -    31.2991 [     0]:
       31.2991 -    70.3646 [     5]:
       70.3646 -   148.4956 [    11]: ∎
      148.4956 -   304.7576 [    15]: ∎∎
      304.7576 -   617.2815 [    35]: ∎∎∎∎∎
      617.2815 -  1242.3294 [    51]: ∎∎∎∎∎∎∎∎
     1242.3294 -  2492.4252 [   128]: ∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎
     2492.4252 -  4992.6168 [   269]: ∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎
     4992.6168 -  9993.0000 [   483]: ∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎

percentile.py
-------------

Calculate percentiles of a stream of decimal values (95% by default).

This is useful for finding response-time percentiles from access logs.

Example (assuming response time is the last column in your access log):

    $ percentile.py -c -1 < /path/to/access.log
    0.412

    $ percentile.py -c -1 -p 50,90,99,99.9 --summary < /path/to/access.log
    count	10000
    min	0.002
    max	3.870
    mean	0.1873
    p50	0.121
    p90	0.305
    p99	0.980
    p99.9	2.410

ninety_five_percent.py
----------------------

The original single-purpose version of `percentile.py`: outputs the 95% value.

    $ awk '{print $NF}' /path/to/access.log | ninety_five_percent.py
    
sample.py
---------

Filter a stream to a random sub-sample of the stream

Example:

    $ cat access.log | sample.py 10% | post_process.py

Rates can be fractional (`0.1%` or `1/1000`), and `--seed N` makes the sample reproducible.

run_for.py
----------

Pass through data for a specified amount of time

Example:

    $ tail -f access.log | run_for.py 10s | post_process.py

bar_chart.py
------------

Generate an ascii bar chart for input data (this is like a visualization of `uniq -c`)

    $ cat data | bar_chart.py
    # each ∎ represents a count of 1. total 63
    14:40 [    49] ∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎
    14:41 [    14] ∎∎∎∎∎∎∎∎∎∎∎∎∎∎

`bar_chart.py` and `histogram.py` also support ingesting pre-aggregated values. Simply provide a two column input of `count<whitespace>value` for `-a` or `value<whitespace>count` for `-A`:

    $ sort /path/to/data | uniq -c | bar_chart.py -a

This is very convenient if you pull data out, say Hadoop or MySQL already aggregated.
