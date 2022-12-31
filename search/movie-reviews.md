# Movie Reviews

Get New York Times reviews, you can search using keywords and optionally define other search criteria

## Usage

```python
NYTAPI.movie_reviews(keyword=None, options=None, dates=None)
```

### Parameters

| Variables                             | Description                          | Data type | Required |
| ------------------------------------- | ------------------------------------ | --------- | -------- |
| `keyword`                             | Reviews of movies with this keyword  | `str`     | False    |
| [`options`](movie-reviews.md#options) | Dictionary of search options         | `dict`    | False    |
| ``[`dates`](movie-reviews.md#dates)`` | Dictionary of dates about the review | `dict`    | False    |

#### **`options`**

| Variables      | Description                                                                     | Data type | Required |
| -------------- | ------------------------------------------------------------------------------- | --------- | -------- |
| `order`        | How to sort the results (`by-title`, `by-publication-date`or `by-opening-date`) | `str`     | False    |
| `reviewer`     | Name of the reviewer                                                            | `str`     | False    |
| `critics_pick` | Only return critics' pick if `True`                                             | `bool`    | False    |

#### **`dates`**

| Variables                | Description                                          | Data type           | Required |
| ------------------------ | ---------------------------------------------------- | ------------------- | -------- |
| `opening_date_start`     | Reviews about movies released at or after this date  | `datetime.datetime` | False    |
| `opening_date_end`       | Reviews about movies released at or before this date | `datetime.datetime` | False    |
| `publication_date_start` | Reviews released at or after this date               | `datetime.datetime` | False    |
| `publication_date_end`   | Reviews released at or before this date              | `datetime.datetime` | False    |

## Example

```python
import datetime

reviews = nyt.movie_reviews(
    keyword = "Green Book",
    options = {
        "order": "by-opening-date",
        "reviewer": "A.O. Scott",
        "critics_pick": False
    },
    dates = {
        "opening_date_start": datetime.datetime(2017, 1, 1),
        "opening_date_end": datetime.datetime(2019, 1, 1),
        "publication_date_start": datetime.datetime(2017, 1, 1),
        "publication_date_end": datetime.datetime(2019, 1, 1)
})
```
