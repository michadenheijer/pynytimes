# Most Viewed

Load the most viewed articles.

## Usage

```python
NYTAPI.most_viewed(days=1)
```

### Parameters

| Variables | Description                                                  | Data type | Required | Default |
| --------- | ------------------------------------------------------------ | --------- | -------- | ------- |
| `days`    | Get most viewed articles over the last `1`, `7` or `30` days | `int`     | False    | `1`     |

## Example

```python
most_viewed = nyt.most_viewed()

# Get most viewed articles of last 7 or 30 days
most_viewed = nyt.most_viewed(days = 7)
most_viewed = nyt.most_viewed(days = 30)
```
