# Automatic Connection

If you want to automatically close the connection then usage using the `with` statement is supported.

```python
with NYTAPI("Your API Key", parse_dates=True) as nyt:
    nyt.most_viewed()
```
