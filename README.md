# Agent Benchmark Exploration

An environment and marimo notebook for the exploration of SWE-bench and Terminal-bench.

## Setup

Make sure you have `uv` installed.

The SWE-bench dataset is retrieved by the notebook via HuggingFace using [`datasets`](https://github.com/huggingface/datasets).

Terminal-bench doesn't have a standard HuggingFace dataset.
It wants users to use [harbor](https://github.com/harbor-framework/harbor), but that's a whole agent-running framework and is a bit too bulky, so instead the Terminal-bench task repo is added here as a git submodule (hence the `--recursive` flag below).

```
git clone --recursive git@github.com:gnodar01/ai-benchmarks.git

uv sync
uv run marimo edit explore.py
```

To clean up afterwards you may want to delete the HuggingSpace-derived SWE-bench dataset from cache (`< 8 MB`):

```
rm -r ~/.cache/huggingface/datasets/SWE-bench___swe-bench_verified
```

