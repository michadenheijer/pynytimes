# Book Reviews

Find New York Times book reviews, you can either search using the author, isbn, or title.&#x20;

## Usage

```python
NYTAPI.book_reviews(author=None, isbn=None, title=None)
```

### Parameters

| Variables | Description                       | Data type | Required           |
| --------- | --------------------------------- | --------- | ------------------ |
| `author`  | Reviews of books from this author | `str`     | One of these three |
| `isbn`    | Reviews of books with this ISBN   | `str`     | One of these three |
| `title`   | Reviews of books with this title  | `str`     | One of these three |

## Example

```python
# Get reviews by author (first and last name)
reviews = nyt.book_reviews(author = "George Orwell")

# Get reviews by ISBN
reviews = nyt.book_reviews(isbn = 9780062963673)

# Get book reviews by title
reviews = nyt.book_reviews(title = "Becoming")
```
