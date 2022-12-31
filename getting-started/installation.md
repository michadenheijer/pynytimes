# Installation

## Default

There are multiple options to install and upgrade pynytimes, but the easiest is by just installing it using `pip` (or `pip3`). Make sure that you are installing pynytimes to the correct Python version.

### Linux and Mac

```bash
pip install --upgrade pynytimes
```

### Windows

```shell
python -m pip install --upgrade pynytimes
```

## Development

You can also install `pynytimes` manually from GitHub itself. This can be done by cloning this repository first, and then installing it using Python.&#x20;

_Note: This might install an unreleased version, installation using this method is only advised if you want to modify the code or help maintain this library._

```bash
git clone https://github.com/michadenheijer/pynytimes.git
cd pynytimes
python setup.py install
```

## Older Python versions

The current version of `pynytimes` only supports the most recent Python versions (3.9, 3.10, and 3.11) however you still might be running older versions of Python. Luckily most of `pynytimes` features are still available. In the table below you can see which version of `pynytimes` still supports your Python version.

| Python version | pynytimes version | Missing features                         |
| -------------- | ----------------- | ---------------------------------------- |
| 3.8            | `0.8.0`           | Some type hings, small bugfixes          |
| 3.7            | `0.7.0`           | Some type hints, small bugfixes          |
| 3.6            | `0.6.1`           | Type hints, small bugfixes, `with` usage |
| 3.5            | `0.4.2`           | Times Tags, no date parsing              |

You can install an older version by `pip install --upgrade pynytimes==0.7.0`.
