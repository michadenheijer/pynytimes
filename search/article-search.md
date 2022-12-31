# Article Search

Find articles that match search criteria.

## Usage

```python
NYTAPI.article_search(query=None, dates=None, options=None, results=10)
```

### Parameters

| Variables                                  | Description                                                               | Data type | Required |
| ------------------------------------------ | ------------------------------------------------------------------------- | --------- | -------- |
| `query`                                    | What you want to search for                                               | `str`     | False    |
| `results`                                  | The amount of results that you want to receive (returns a multiple of 10) | `int`     | False    |
| ``[`dates`](article-search.md#dates)``     | A dictionary of the dates you'd like the results to be between            | `dict`    | False    |
| ``[`options`](article-search.md#options)`` | A dictionary of additional options                                        | `dict`    | False    |

#### **`dates`**

| Variables | Description                                        | Data type                              | Required |
| --------- | -------------------------------------------------- | -------------------------------------- | -------- |
| `begin`   | Results should be published at or after this date  | `datetime.datetime` or `datetime.date` | False    |
| `end`     | Results should be published at or before this date | `datetime.datetime` or `datetime.date` | False    |

#### **`options`**

| Variables          | Description                                                                                                                                                             | Data type | Required |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------- | -------- |
| `sort`             | How you want the results to be sorted (`oldest`, `newest` or `relevance`)                                                                                               | `str`     | False    |
| `sources`          | Results should be from one of these sources                                                                                                                             | `list`    | False    |
| `news_desk`        | Results should be from one of these news desks ([valid options](https://github.com/michadenheijer/pynytimes/blob/main/VALID\_SEARCH\_OPTIONS.md#news-desk-values))      | `list`    | False    |
| `type_of_material` | Results should be from this type of material ([valid options](https://github.com/michadenheijer/pynytimes/blob/main/VALID\_SEARCH\_OPTIONS.md#type-of-material-values)) | `list`    | False    |
| `section_name`     | Results should be from this section ([valid options](https://github.com/michadenheijer/pynytimes/blob/main/VALID\_SEARCH\_OPTIONS.md#section-name-values))              | `list`    | False    |

## Example

```python
import datetime

articles = nyt.article_search(
    query = "Obama", # Search for articles about Obama
    results = 30, # Return 30 articles
    # Search for articles in January and February 2019
    dates = {
        "begin": datetime.datetime(2019, 1, 31),
        "end": datetime.datetime(2019, 2, 28)
    },
    options = {
        "sort": "oldest", # Sort by oldest options
        # Return articles from the following four sources
        "sources": [
            "New York Times",
            "AP",
            "Reuters",
            "International Herald Tribune"
        ],
        # Only get information from the Politics desk
        "news_desk": [
            "Politics"
        ],
        # Only return News Analyses
        "type_of_material": [
            "News Analysis"
        ]
    }
)
```
