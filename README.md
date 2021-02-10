# pynytimes

[<img src="https://raw.githubusercontent.com/michadenheijer/pynytimes/main/.github/poweredby_nytimes.png" height="20px">](https://developer.nytimes.com/) [![Build Status](https://travis-ci.com/michadenheijer/pynytimes.svg?token=8nhCHVYqgufX65p8PRDx&branch=main)](https://travis-ci.com/michadenheijer/pynytimes) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pynytimes)](https://pypi.org/project/pynytimes/) [![PyPI](https://img.shields.io/pypi/v/pynytimes)](https://pypi.org/project/pynytimes/)

Use all (actually most) New York Times APIs, get all the data you need from the Times!

## Installation

There are multiple options to install and ugprade pynytimes, but the easiest is by just installing it using ```pip``` (or ```pip3```). *You can also optionally install ```orjson``` for faster json parsing.*

### Linux and Mac

```bash
pip install --upgrade pynytimes
```

### Windows

```shell
python -m pip install --upgrade pynytimes
```

### Development

You can also install ```pynytimes``` manually from GitHub itself. This can be done by cloning this repository first, and then installing it using Python. *This might install an unreleased version, installation using this method is only advised if you want to modify the code or help maintain this library.*

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
nyt = NYTAPI("Your API key", parse_dates=True)
```

**Optionally you can also set to use ```http``` instead of ```https```.**
```python
nyt = NYTAPI("Your API key", https=False)
```


| Variables        | Description                                                           | Data type                       | Required |
|------------------|-----------------------------------------------------------------------|---------------------------------|----------|
| ```key```        | The API key from [The New York Times](https://developer.nytimes.com/) | ```str```                       | True     |
| ```https```      | Whether you'd want requests over https                                | ```bool```                      | False    |
| ```session```    | A requests session that you'd like the wrapper to use                 | ```requests.sessions.Session``` | False    |
| ```backoff```    | Enable [exponential backoff](https://en.wikipedia.org/wiki/Exponential_backoff) | ```bool```            | False    |
| ```user_agent``` | The user agent that the client uses                                   | ```str```                       | False    |
| ```parse_dates```| Optionally disable the automatic parsing of dates (usually this is disabled) | ```bool```                | False    |

### Supported APIs

When you have imported this library you can use the following features from the New York Times API.
- [Top stories](#top-stories)
- [Most viewed articles](#most-viewed-articles)
- [Most shared articles](#most-shared-articles)
- [Article search](#article-search)
- [Book reviews](#book-reviews)
- [Movie reviews](#movie-reviews)
- [Best sellers lists](#best-sellers-lists)
- [Article metadata (Times Wire)](#article-metadata)
- [Load latest articles (Times Wire)](#load-latest-articles)
- [Tag query (TimesTags)](#tag-query)
- [Archive metadata](#archive-metadata)


### Top stories

You can request the top stories from the New York Times. You can also get the top stories from a specific section.

```python
top_stories = nyt.top_stories()

# Get all the top stories from a specific category
top_science_stories = nyt.top_stories(section = "science")
```


| Variables       | Description                             | Data type       | Required |
|-----------------|-----------------------------------------|-----------------|----------|
| ```section```   | Get Top Stories from a specific section | ```str```       | False    |

The possible sections are: arts, automobiles, books, business, fashion, food, health, home, insider, magazine, movies, national, nyregion, obituaries, opinion, politics, realestate, science, sports, sundayreview, technology, theater, tmagazine, travel, upshot, and world.


### Most viewed articles

The New York Times API can provide the most popular articles from the last day, week or month.

```python
most_viewed = nyt.most_viewed()

# Get most viewed articles of last 7 or 30 days
most_viewed = nyt.most_viewed(days = 7)
most_viewed = nyt.most_viewed(days = 30)
```


| Variables       | Description                                                              | Data type       | Required |
|-----------------|--------------------------------------------------------------------------|-----------------|----------|
| ```days```      | Get most viewed articles over the last ```1```, ```7``` or ```30``` days | ```int```       | False    |


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


| Variables       | Description                                                              | Data type       | Required |
|-----------------|--------------------------------------------------------------------------|-----------------|----------|
| ```days```      | Get most viewed articles over the last ```1```, ```7``` or ```30``` days | ```int```       | False    |
| ```method```    | Method of sharing (```email``` or ```facebook```)                        | ```str```       | False    |



### Article search

You can also search all New York Times articles. Optionally you can define your search query (using the ```query``` option), the amount of results (using ```results```) and the amount of results you'd like. You can even add more options so you can filter the results.

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
        "sort": "oldest",
        "sources": [
            "New York Times",
            "AP",
            "Reuters",
            "International Herald Tribune"
        ],
        "news_desk": [
            "Politics"
        ],
        "type_of_material": [
            "News Analysis"
        ]
    }
)
```

| Variables                   | Description                                                                           | Data type       | Required |
|-----------------------------|---------------------------------------------------------------------------------------|-----------------|----------|
| ```query```                 | What you want to search for                                                           | ```str```       | False    |
| ```results```               | The amount of results that you want to receive (returns a multiple of 10)             | ```int```       | False    |
| [```dates```](#dates)       | A dictionary of the dates you'd like the results to be between                        | ```dict```      | False    |
| [```options```](#options)   | A dictionary of additional options                                                    | ```dict```      | False    |

#### ```dates```

| Variables       | Description                                        | Data type               | Required |
|-----------------|----------------------------------------------------|-------------------------|----------|
| ```begin```     | Results should be published at or after this date  | ```datetime.datetime``` | False    |
| ```end```       | Results should be published at or before this date | ```datetime.datetime``` | False    |

#### ````options````

| Variables               | Description                                                                                                     | Data type       | Required |
|-------------------------|-----------------------------------------------------------------------------------------------------------------|-----------------|----------|
| ```sort```              | How you want the results to be sorted (```oldest```, ```newest``` or ```relevance```)                           | ```str```       | False    |
| ```sources```           | Results should be from one of these sources                                                                     | ```list```      | False    |
| ```news_desk```         | Results should be from one of these news desks ([valid options](VALID_SEARCH_OPTIONS.md#news-desk-values))      | ```list```      | False    |
| ```type_of_material```  | Results should be from this type of material ([valid options](VALID_SEARCH_OPTIONS.md#type-of-material-values)) | ```list```      | False    |
| ```section_name```      | Results should be from this section ([valid options](VALID_SEARCH_OPTIONS.md#section-name-values))              | ```list```      | False    |


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

| Variables     | Description                       | Data type | Required           |
|---------------|-----------------------------------|-----------|--------------------|
| ```author```  | Reviews of books from this author | ```str``` | One of these three |
| ```isbn```    | Reviews of books with this ISBN   | ```str``` | One of these three |
| ```title```   | Reviews of books with this title  | ```str``` | One of these three |

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

| Variables     | Description                          | Data type  | Required           |
|---------------|--------------------------------------|------------|--------------------|
| ```keyword``` | Reviews of movies with this keyword  | ```str```  | False              |
| ```options``` | Dictionary of search options         | ```dict``` | False              |
| ```dates```   | Dictionary of dates about the review | ```dict``` | False              |

#### ```options```

| Variables          | Description                                                                                 | Data type   | Required |
|--------------------|---------------------------------------------------------------------------------------------|-------------|----------|
| ```order```        | How to sort the results (```by-title```, ```by-publication-date```or ```by-opening-date```) | ```str```   | False    |
| ```reviewer```     | Name of the reviewer                                                                        | ```str```   | False    |
| ```critics_pick``` | Only return critics' pick if ```True```                                                     | ```bool```  | False    |

#### ```dates```

| Variables                    | Description                                           | Data type                | Required |
|------------------------------|-------------------------------------------------------|--------------------------|----------|
| ```opening_date_start```     | Reviews about movies released at or after this date   | ```datetime.datetime```  | False    |
| ```opening_date_end```       | Reviews about movies released at or before this date  | ```datetime.datetime```  | False    |
| ```publication_date_start``` | Reviews released at or after this date                | ```datetime.datetime```  | False    |
| ```publication_date_end```   | Reviews released at or before this date               | ```datetime.datetime```  | False    |

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

| Variables   | Description               | Data type               | Required |
|-------------|---------------------------|-------------------------|----------|
| ```name```  | Name of best sellers list | ```str```               | False    |
| ```date```  | Date of best sellers list | ```datetime.datetime``` | False    |

### Article metadata

With an URL from a New York Times article you can easily get all the metadata you need from it.

```python
metadata = nyt.article_metadata(
    url = "https://www.nytimes.com/2019/10/20/world/middleeast/erdogan-turkey-nuclear-weapons-trump.html"
)
```

| Variables | Description        | Data type  | Required |
|-----------|--------------------|------------|----------|
| ```url``` | URL of the article | ```str```  | True     |

### Load latest articles

You can easily load the latest articles published by the New York Times. 

```python
latest = nyt.latest_articles(
    source = "nyt",
    section = "books"
)
```

| Variables     | Description                                              | Data type  | Required |
|---------------|----------------------------------------------------------|------------|----------|
| ```source```  | Source of article (```all```, ```nyt``` and ```inyt```)  | ```str```  | False    |
| ```section``` | Section of articles                                      | ```str```  | False    |

You can find all possible sections using:
```python
sections = nyt.section_list()
```

### Tag query

The New York Times has their own tags library. You can query this library with this API.

```python
tags = nyt.tag_query(
    "pentagon",
    max_results = 20
)
```

| Variables            | Description                | Data type  | Required |
|----------------------|----------------------------|------------|----------|
| ```query```          | Tags you're looking for    | ```str```  | True     |
| ```max_results```    | Maximum results you'd like | ```int```  | False    |
| ```filter_options``` | Filter options             | ```list``` | False    |

### Archive metadata

If you want to load all the metadata from a specific month, then this API makes that possible. Be aware you'll download a big JSON file (about 20 Mb), so it can take a while.

```python
import datetime

data = nyt.archive_metadata(
    date = datetime.datetime(2019, 1, 1)
)
```

| Variables  | Description                       | Data type               | Required |
|------------|-----------------------------------|-------------------------|----------|
| ```date``` | Date of month of all the metadata | ```datetime.datetime``` | True     |

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Disclaimer**: *This project is not made by anyone from the New York Times, nor is it affiliated with The New York Times Company.*
