# Best Sellers Lists

Load best seller list.

## Usage

```python
NYTAPI.best_sellers_list(name="combined-print-and-e-book-fiction", date=None)
```

### Parameters

| Variables | Description               | Data type           | Required | Default                               |
| --------- | ------------------------- | ------------------- | -------- | ------------------------------------- |
| `name`    | Name of best sellers list | `str`               | False    | `"combined-print-and-e-book-fiction"` |
| `date`    | Date of best sellers list | `datetime.datetime` | False    | Today                                 |

#### `name`

Get all best sellers lists

```
lists = nyt.best_sellers_lists()
```

## Example

```python
# Get fiction best sellers list
books = nyt.best_sellers_list()

# Get non-fiction best sellers list
books = nyt.best_sellers_list(
    name = "combined-print-and-e-book-nonfiction"
)

# Get best sellers lists from other date
import datetime

books = nyt.best_sellers_list(
    name = "combined-print-and-e-book-nonfiction",
    date = datetime.datetime(2019, 1, 1)
)
```
