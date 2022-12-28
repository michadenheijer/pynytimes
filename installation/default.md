# Default

There are multiple options to install and ugprade pynytimes, but the easiest is by just installing it using `pip` (or `pip3`). This should automatically install the latest available version compatible with your Python version.

## Linux and Mac

```bash
pip install --upgrade pynytimes
```

## Windows

```shell
python -m pip install --upgrade pynytimes
```

## Older Python versions

The current version of `pynytimes` only supports the most recent Python versions (3.9, 3.10, and 3.11) however you still might be running older versions of Python. Luckily most of `pynytimes` features are still available. In the table below you can see which version of `pynytimes` still supports your Python version.

| Python version | `pynytimes` version | Missing features                         |
| -------------- | ------------------- | ---------------------------------------- |
| 3.7            | `0.7.0`             | Some type hints, small bugfixes          |
| 3.6            | `0.6.1`             | Type hints, small bugfixes, `with` usage |
| 3.5            | `0.4.2`             | Times Tags, no date parsing              |

You can install an older version by `pip install --upgrade pynytimes==0.7.0`.
