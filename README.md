# pynytimes

[<img src="https://raw.githubusercontent.com/michadenheijer/pynytimes/main/.github/poweredby_nytimes.png" height="20px">](https://developer.nytimes.com/) [![Run full tests](https://github.com/michadenheijer/pynytimes/actions/workflows/python-full-tests.yaml/badge.svg)](https://github.com/michadenheijer/pynytimes/actions/workflows/python-full-tests.yaml)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pynytimes)](https://pypi.org/project/pynytimes/) [![PyPI](https://img.shields.io/pypi/v/pynytimes)](https://pypi.org/project/pynytimes/) [![Downloads](https://pepy.tech/badge/pynytimes)](https://pepy.tech/project/pynytimes) [![DOI](https://zenodo.org/badge/216087297.svg)](https://zenodo.org/badge/latestdoi/216087297)

Use all (actually most) New York Times APIs, get all the data you need from the Times!

## Documentation

Extensive documentation is available at: https://pynytimes.michadenheijer.com/.

## Installation

There are multiple options to install and upgrade pynytimes, but the easiest is by just installing it using ```pip``` (or ```pip3```).
### Linux and Mac

```bash
pip install --upgrade pynytimes
```

### Windows

```shell
python -m pip install --upgrade pynytimes
```

## Usage

You can easily import this library using:

```python
from pynytimes import NYTAPI
```

Then you can simply add your API key (get your API key from [The New York Times Dev Portal](https://developer.nytimes.com/)):

```python
nyt = NYTAPI("Your API key", parse_dates=True)
```

**Make sure that if you commit your code to GitHub you [don't accidentially commit your API key](https://towardsdatascience.com/how-to-hide-your-api-keys-in-python-fb2e1a61b0a0).**

## Supported APIs

When you have imported this library you can use the following features from the New York Times API.

**Search**
- [Article search](https://pynytimes.michadenheijer.com/search/article-search)
- [Book reviews](https://pynytimes.michadenheijer.com/search/book-reviews)
- [Movie reviews](https://pynytimes.michadenheijer.com/search/movie-reviews)

**Popular**
- [Top stories](https://pynytimes.michadenheijer.com/popular/top-stories)
- [Most viewed articles](https://pynytimes.michadenheijer.com/popular/most-viewed)
- [Most shared articles](https://pynytimes.michadenheijer.com/popular/most-shared)
- [Best sellers lists](https://pynytimes.michadenheijer.com/popular/best-sellers-lists)

**Metadata**
- [Article metadata](https://pynytimes.michadenheijer.com/metadata/article-metadata)
- [Archive metadata](https://pynytimes.michadenheijer.com/metadata/archive-metadata)
- [Load latest articles](https://pynytimes.michadenheijer.com/metadata/latest-articles)

**Other**
- [Tag query (TimesTags)](https://pynytimes.michadenheijer.com/other/tags)

### Top stories

To get the current top stories use:

```python
top_stories = nyt.top_stories()
```
Read [the documentation](https://pynytimes.michadenheijer.com/popular/top-stories) to find the top stories per section.

### Most viewed articles

You can also get todays most viewed articles:

```python
most_viewed = nyt.most_viewed()
```
Read [the documentation](https://pynytimes.michadenheijer.com/popular/most-viewed) to get the most viewed articles per week or month.

### Most shared articles

To get the most shared articles (shared over email) use:

```python
most_shared = nyt.most_shared()
```

Read [the documentation](https://pynytimes.michadenheijer.com/popular/most-shared) to get the most shared articles using facebook.


### Article search

Search articles using a query using:

```python
articles = nyt.article_search(query="Obama")
```
In this example we have just defined the content of the search query (Obama), but we can add many more search parameters. Read [the documentation](https://pynytimes.michadenheijer.com/search/article-search) to see how.


### Book reviews

You can easily find book reviews for every book you've read. You can find those reviews by searching for the author, ISBN or title of the book.

```python
# Get reviews by author (first and last name)
reviews = nyt.book_reviews(author="George Orwell")

# Get reviews by ISBN
reviews = nyt.book_reviews(isbn="9780062963673")

# Get book reviews by title
reviews = nyt.book_reviews(title="Becoming")
```

Read [the documentation](https://pynytimes.michadenheijer.com/search/book-reviews) to find more information about additional parameters.

### Movie reviews

You can not only get the book reviews, but the movie reviews too.

```python
reviews = nyt.movie_reviews(keyword="Green Book")
```

Read [the documentation](https://pynytimes.michadenheijer.com/search/movie-reviews) to find more information about additional parameters.

### Best sellers lists

The New York Times has multiple best sellers lists. To get from the fiction best seller list:

```python
# Get fiction best sellers list
books = nyt.best_sellers_list()
```

Read how to get the other best seller lists in [the documentation](https://pynytimes.michadenheijer.com/popular/best-sellers-lists).

### Article metadata

With an URL from a New York Times article you can easily get all the metadata you need from it.

```python
metadata = nyt.article_metadata(
    url = "https://www.nytimes.com/2019/10/20/world/middleeast/erdogan-turkey-nuclear-weapons-trump.html"
)
```
Read additional parameters in [the documentation](https://pynytimes.michadenheijer.com/metadata/article-metadata).

### Load latest articles

You can easily load the latest articles published by the New York Times.

```python
latest = nyt.latest_articles(
    source = "nyt",
    section = "books"
)
```

Additional parameters can be found in [the documentation](https://pynytimes.michadenheijer.com/metadata/latest-articles).

### Tag query

The New York Times has their own tags library. You can query this library with this API.

```python
tags = nyt.tag_query(
    "pentagon",
    max_results = 20
)
```

Additional parameters can be found in [the documentation](https://pynytimes.michadenheijer.com/other/tags).

### Archive metadata

If you want to load all the metadata from a specific month, then this API makes that possible. Be aware you'll download a big JSON file (about 20 Mb), so it can take a while.

```python
import datetime

data = nyt.archive_metadata(
    date = datetime.datetime(2019, 1, 1)
)
```

[Read more in the documentation](https://pynytimes.michadenheijer.com/metadata/archive-metadata).

## Citing this Repository
If you use ```pynytimes```, a citation would be very much appriciated. If you're using BibTeX you can use the following citation:

```bib
@software{Den_Heijer_pynytimes_2023,
    author = {Den Heijer, Micha},
    license = {MIT},
    title = {{pynytimes}},
    url = {https://github.com/michadenheijer/pynytimes},
    version = {0.10.1},
    year = {2023},
    doi = {10.5281/zenodo.7821090}
}
```

If you're not using BibTeX, you can [retrieve the preferred citation from Zenodo](https://doi.org/10.5281/zenodo.7821090).

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Disclaimer**: *This project is not made by anyone from the New York Times, nor is it affiliated with The New York Times Company.*
