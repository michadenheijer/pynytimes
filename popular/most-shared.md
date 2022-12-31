# Most Shared

Load most shared articles.

## Usage

```
NYTAPI.most_shared(days=1, method="email")
```

### Parameters

| Variables | Description                                                  | Data type | Required | Default   |
| --------- | ------------------------------------------------------------ | --------- | -------- | --------- |
| `days`    | Get most viewed articles over the last `1`, `7` or `30` days | `int`     | False    | `1`       |
| `method`  | Method of sharing (`email` or `facebook`)                    | `str`     | False    | `"email"` |

## Example

```python
most_shared = nyt.most_shared()

# Get most emailed articles of the last day
most_shared = myt.most_shared(
    days = 1,
    method = "email"
)

# Get most shared articles to Facebook of the last 7 days
most_shared = nyt.most_shared(
    days = 7,
    method = "facebook"    
)

# Get most shared articles to Facebook of the last 30 days
most_shared = nyt.most_shared(
    days = 30,
    method = "facebook"
)
```
