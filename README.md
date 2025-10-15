[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/id8-engineering/python-em511/badge)](https://scorecard.dev/viewer/?uri=github.com/id8-engineering/python-em511)

# python-em511

Driver for Carlo Gavazzi EM511 Series Single Phase Energy Meters using Modbus RTU.

## Get started

### Prerequisites

* Install [Python (>=3.10)](https://www.python.org/downloads/)
* Install [git](https://git-scm.com/downloads)
* Install [uv](https://docs.astral.sh/uv/getting-started/installation/)

### Setup development environment

Clone the repository:

```sh
git clone git@github.com:id8-engineering/python-em511.git
```

Change directory:

```sh
cd python-em511
```

Run pre-commit tests:

```sh
uv run pre-commit run -a
```

Build package:

```sh
uv build
```
