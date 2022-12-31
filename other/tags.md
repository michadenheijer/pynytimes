# Tags

Load New York Times tags.

## Usage

```python
NYTAPI.tag_query(query, max_results=20, filter_options=None)
```

### Parameters

| Variables        | Description                | Data type | Required | Default |
| ---------------- | -------------------------- | --------- | -------- | ------- |
| `query`          | Tags you're looking for    | `str`     | True     |         |
| `max_results`    | Maximum results you'd like | `int`     | False    | `20`    |
| `filter_options` | Filter options             | `list`    | False    |         |

## Example

```python
tags = nyt.tag_query(
    "pentagon",
    max_results = 20
)
```
