# pynytimes

[<img src="https://raw.githubusercontent.com/michadenheijer/pynytimes/main/.github/poweredby_nytimes.png" height="20px">](https://developer.nytimes.com/) [![Build Status](https://travis-ci.com/michadenheijer/pynytimes.svg?token=8nhCHVYqgufX65p8PRDx&branch=main)](https://travis-ci.com/michadenheijer/pynytimes) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) ![PyPI](https://img.shields.io/pypi/v/pynytimes)

Use all (actually most) New York Times APIs, get all the data you need from the Times!

## Installation

There are multiple options to install pynytimes, but the easiest is by just installing it using pip (or pip3).

```bash
pip install pynytimes
```

### Advanced (not better, just different)

You can also install pynytimes manually from GitHub itself. This can be done by cloning this repository first, and then installing it using Python. *This might install an unreleased version, installation using this method is only advised if you want to modify the code or help maintain this library.*

```bash
git clone https://github.com/michadenheijer/pynytimes.git
cd pynytimes
python setup.py install
```

## Usage

You can easily import this library using:

```python
from pynytimes import NYTAPI
```

Then you can simply add your API key (get your API key from [The New York Times Dev Portal](https://developer.nytimes.com/)):

```python
nyt = NYTAPI("Your API key")
```

When you have imported this library you can use the following features from the New York Times API.
- [Top stories](#top-stories)
- [Most viewed articles](#most-viewed-articles)
- [Most shared articles](#most-shared-articles)
- [Article search](#article-search-beta)
- [Book reviews](#book-reviews)
- [Movie reviews](#movie-reviews)
- [Best sellers lists](#best-sellers-lists)
- [Article metadata (Times Wire)](#article-metadata)
- [Tag query (TimesTags)](#tag-query)
- [Archive metadata](#archive-metadata)

### Top stories

You can request the top stories from the New York Times. You can also get the top stories from a specific section.

```python
top_stories = nyt.top_stories()

# Get all the top stories from a specific category
top_science_stories = nyt.top_stories(section = "science")
```

The possible sections are: arts, automobiles, books, business, fashion, food, health, home, insider, magazine, movies, national, nyregion, obituaries, opinion, politics, realestate, science, sports, sundayreview, technology, theater, tmagazine, travel, upshot, and world.

### Most viewed articles

The New York Times API can provide the most popular articles from the last day, week or month.

```python
most_viewed = nyt.most_viewed()

# Get most viewed articles of last 7 or 30 days
most_viewed = nyt.most_viewed(days = 7)
most_viewed = nyt.most_viewed(days = 30)
```

### Most shared articles

Not only can you request the most viewed articles from the New York Times API, you can also request the most shared articles. You can even request the articles that are most shared by email and Facebook. You can get the most shared articles per day, week or month.

```python
most_shared = nyt.most_shared()

# Get most emaild articles of the last day
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

### Article search (beta)

You can also search all New York Times articles. You can also define which sources you want to include. (Not all functions are implemented)

```python
import datetime

articles = nyt.article_search(
    query = "Obama",
    results = 30,
    dates = {
        "begin": datetime.datetime(2019, 1, 31),
        "end": datetime.datetime(2019, 2, 28)
    },
    options = {
        sources = [
            "New York Times",
            "AP",
            "Reuters",
            "International Herald Tribune"
        ]
    }
)
```

### Book reviews

You can easily find book reviews for every book you've read. You can find those reviews by searching for the author, ISBN or title of the book.

```python
# Get reviews by author (first and last name)
reviews = nyt.book_reviews(author = "George Orwell")

# Get reviews by ISBN
reviews = nyt.book_reviews(isbn = 9780062963673)

# Get book reviews by title
reviews = nyt.book_reviews(title = "Becoming")
```

### Movie reviews

You can not only get the book reviews, but the movie reviews too.

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

### Best sellers lists

The New York Times has multiple best sellers lists. You can easily request those lists using this library.

```python
# Get all the available New York Times best sellers lists
lists = nyt.best_sellers_lists()

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

### Article metadata

With an URL from a New York Times article you can easily get all the metadata you need from it.

```python
metadata = nyt.article_metadata(
    url = "https://www.nytimes.com/2019/10/20/world/middleeast/erdogan-turkey-nuclear-weapons-trump.html"
)
```

### Tag query

The New York Times has their own tags library. You can query this library with this API.

```python
tags = nyt.tag_query(
    "pentagon",
    max_results = 20
)
```

### Archive metadata

If you want to load all the metadata from a specific month, then this API makes that possible. Be aware you'll download a big JSON file (about 20 Mb), so it can take a while.

```python
import datetime

data = nyt.archive_metadata(
    date = datetime.datetime(2019, 1, 1)
)
```

## License

[MIT](LICENSE)

**Disclaimer**: *This project is not made by anyone from the New York Times, nor is it affiliated with The New York Times Company.*
