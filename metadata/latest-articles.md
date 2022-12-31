# Latest Articles

Load metadata of the latest articles.

## Usage

```python
NYTAPI.latest_articles(source=None, section=None)
```

### Parameters

| Variables                                   | Description                                 | Data type | Required | Default |
| ------------------------------------------- | ------------------------------------------- | --------- | -------- | ------- |
| `source`                                    | Source of article (`all`, `nyt` and `inyt`) | `str`     | False    | `"all"` |
| ``[`section`](latest-articles.md#section)`` | Section of articles                         | `str`     | False    |         |

#### `section`

You can find all possible sections using:

```python
sections = nyt.section_list()
```

## Example

```python
latest = nyt.latest_articles(
    source = "nyt",
    section = "books"
)
```
