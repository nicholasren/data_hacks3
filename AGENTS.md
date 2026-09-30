# AGENTS.md

Guidance for AI coding agents working in this repository.

## What this is

`data_hacks3` is a Python 3 port of [bitly/data_hacks](https://github.com/bitly/data_hacks):
a handful of small, standalone command-line filters for quick data analysis in
Unix pipelines. Published to PyPI as `data_hacks3`.

This repo is a GitHub fork of `bitly/data_hacks`. Keep an `upstream` remote
pointing at `https://github.com/bitly/data_hacks.git` and merge
`upstream/master` to pick up upstream fixes.

## Layout

```
data_hacks/          package; one self-contained script per tool, each with a main()
  histogram.py         text histogram; linear, log (-l) or custom (-B) buckets; mean/var/SD/median
  bar_chart.py         ascii bar chart of value counts (visual `uniq -c`)
  percentile.py        percentiles (-p 50,99) and optional summary of a stream of numbers
  ninety_five_percent.py  legacy: 95th percentile only (kept for compatibility)
  sample.py            pass through a random N% (or x/y) of lines; --seed
  run_for.py           pass stdin through for a duration (10s, 5m, 1h, 1d)
pyproject.toml       setuptools packaging; [project.scripts] installs each tool twice
                     (bare name + original *.py name)
go                   build/publish helper: ./go build | test_publish | publish (uv, twine)
README.markdown      user-facing docs and examples (also the PyPI long description)
TODO.md              planned features; tick items off as they land
```

## Conventions

- Each script is standalone: stdlib only (`optparse`, `decimal`, `collections`,
  `math`, `random`, `shutil`). Do not add third-party dependencies or cross-script
  imports; every script must still run as `python3 data_hacks/<tool>.py`. Small
  helpers such as `select_field()` are deliberately duplicated per script.
- Every script's `__main__` block just calls `main()`, which the entry points use.
- Scripts read from stdin and print usage and exit 1 when stdin is a TTY.
  Numeric parsing uses `Decimal`; bad lines are reported to stderr and skipped.
- `histogram.py` and `bar_chart.py` share the aggregated-input flags:
  `-a` = `count value`, `-A` = `value count`, `--dot` for the bar character, and
  `-w/--width` (defaults to `shutil.get_terminal_size()`; bars must never overflow it).
- `histogram.py`, `bar_chart.py` and `percentile.py` share `-c/--column` and
  `-d/--delimiter` (`-f` is taken by `histogram.py --bucket-format`).
- CLI parsing uses `optparse` (legacy, kept to match upstream). Match the existing
  style when adding options.
- Keep the Bitly Apache 2.0 license headers intact.
- Keep changes small and close to upstream so future `upstream/master` merges stay
  clean. Upstream is Python 2/3-agnostic-ish; this fork is Python 3 only
  (`print()` function, `print(..., file=sys.stderr)`).
- When adding a new script, give it a `main()`, add both entry points to
  `[project.scripts]` in `pyproject.toml`, and document it in `README.markdown`.

## Testing

There is no test suite or CI. `histogram.py` contains `test_mvsd()` and
`test_median()` (pytest-style); run them after touching the stats code.

Smoke-test changes by piping data through the scripts:

```sh
seq 1 100 | python3 data_hacks/histogram.py -l -b 4
printf 'a\nb\na\n' | python3 data_hacks/bar_chart.py -p
seq 1 100 | python3 data_hacks/ninety_five_percent.py
seq 1 1000 | python3 data_hacks/percentile.py -p 50,99 -s
seq 1 100 | python3 data_hacks/sample.py 10%
python3 -m pytest data_hacks/histogram.py -k mvsd
```

## Releasing

1. Bump `version` in `pyproject.toml`.
2. `./go build` (creates `dist/` sdist + wheel via `uv build`), then `./go test_publish` or `./go publish`.
