# Article Metadata

Get all metadata from an article.

## Usage

```python
NYTAPI.article_metadata(url)
```

### Parameters

| Variables | Description        | Data type | Required |
| --------- | ------------------ | --------- | -------- |
| `url`     | URL of the article | `str`     | True     |

## Example

```python
metadata = nyt.article_metadata(
    url = "https://www.nytimes.com/2019/10/20/world/middleeast/erdogan-turkey-nuclear-weapons-trump.html"
)
```
