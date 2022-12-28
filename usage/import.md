# Import

You can easily import this library using:

```python
from pynytimes import NYTAPI
```

Then you can simply add your API key (get your API key from [The New York Times Dev Portal](https://developer.nytimes.com/)):

```python
nyt = NYTAPI("Your API key", parse_dates=True)
```

**Make sure that if you commit your code to GitHub you** [**don't accidentially commit your API key**](https://towardsdatascience.com/how-to-hide-your-api-keys-in-python-fb2e1a61b0a0)**.**

| Variables     | Description                                                                      | Data type                   | Required | Default               |
| ------------- | -------------------------------------------------------------------------------- | --------------------------- | -------- | --------------------- |
| `key`         | The API key from [The New York Times](https://developer.nytimes.com/)            | `str`                       | True     | `None`                |
| `https`       | Use [HTTPS](https://en.wikipedia.org/wiki/HTTPS)                                 | `bool`                      | False    | `True`                |
| `session`     | Optionally set your own `request.session`                                        | `requests.sessions.Session` | False    | `requests.Session()`  |
| `backoff`     | Enable [exponential backoff](https://en.wikipedia.org/wiki/Exponential\_backoff) | `bool`                      | False    | `True`                |
| `user_agent`  | Set the [User Agent](https://en.wikipedia.org/wiki/User\_agent)                  | `str`                       | False    | `pynytimes/[version]` |
| `parse_dates` | Enable the parsing of dates into `datetime.datetime` or `datetime.date` objects  | `bool`                      | False    | `False`               |
