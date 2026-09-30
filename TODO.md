# TODO

Planned extensions to data_hacks3. Every tool stays a small, stdlib-only Unix
pipe filter: read stdin, write stdout, print usage when stdin is a TTY.

## Quick wins

- [x] **`percentile.py`**: generalize `ninety_five_percent.py`.
  - `-p/--percentiles 50,90,99,99.9` (default `95`); decimal percentiles allowed.
  - `-s/--summary` also prints count, min, max and mean.
  - A single percentile without `--summary` prints the bare value, like `ninety_five_percent.py`.
  - Keep `ninety_five_percent.py` working for backward compatibility.
- [x] **Column selector**: `-c/--column N` and `-d/--delimiter` on `histogram.py`, `bar_chart.py`
  and `percentile.py`, so `awk '{print $NF}' |` is no longer needed.
  - Fields are 1-based; negative counts from the end (`-c -1` is the last column); `-f` was taken by `histogram.py --bucket-format`.
  - Default delimiter is whitespace. Lines missing the column are reported on stderr and skipped.
  - Not combinable with the `-a`/`-A` aggregated input modes.
- [x] **Terminal-width bars**: `bar_chart.py` and `histogram.py` size bars to the terminal
  (`shutil.get_terminal_size()`, 80 columns when piped) instead of the hardcoded 80/75.
  - `-w/--width` overrides the width.
  - Bars must never overflow the width. `histogram.py` used to floor the scale, so a max
    bucket of 149 drew 149 characters.
- [x] **`sample.py` improvements**:
  - `--seed N` for reproducible samples.
  - Fractional rates: `0.1%` and `1/1000` work (previously the minimum was 1%).
  - The rate is read from the positional argument, not `sys.argv[-1]`, so options may follow it.
- [x] **Packaging**: `pyproject.toml` with `console_scripts` entry points.
  - Installs `histogram`, `bar_chart`, `percentile`, `ninety_five_percent`, `sample` and `run_for`,
    and keeps the `*.py` names for backward compatibility.
  - Each script gets a `main()`, and running `python data_hacks/<tool>.py` directly still works.
  - Replaces `setup.py`. Sets the long description from the README (fixes the `twine check` warnings).

## New tools

- [ ] **`sparkline.py`**: a stream of numbers becomes a single-line sparkline (`▁▂▃▅▇█▅▃`); useful with `tail -f`.
- [ ] **`rate.py`**: counts timestamped lines per second or minute; a live time-bucketed `bar_chart`.
- [ ] **`top_k.py`**: approximate heavy hitters (Misra-Gries / count-min sketch) for streams
  too large for `sort | uniq -c`.
- [ ] **`reservoir.py`**: sample exactly N lines from a stream of unknown length.
- [ ] **`stats.py`**: a one-line summary (count, min, max, mean, SD, p50/p95/p99), reusing the
  running-statistics logic in `histogram.py` (`MVSD`).

## Bigger ideas

- [ ] **Live mode**: `--follow` on `histogram.py` and `bar_chart.py` redraws every N seconds
  while reading from `tail -f`.
- [ ] **Scatter / heatmap**: two-column `x y` input rendered as an ASCII grid.
- [ ] **Test suite + CI**: pytest tests for every tool, run by GitHub Actions on Python 3.9–3.14.
  Highest priority of this section: the Python 3 `median()` bug slipped through because nothing ran the tests.
