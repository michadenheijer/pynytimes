from pynytimes import NYTAPI

import datetime
import os

begin = datetime.datetime.now()

API_KEY = os.environ["NewYorkTimesAPIKey"]
nyt = NYTAPI(API_KEY)

nyt.top_stories(section="science")

nyt.most_viewed(days=30)

nyt.most_shared(
    days = 30,
    method = "email"
)

nyt.book_reviews(
    author = "Michelle Obama"
)

nyt.best_sellers_lists()

nyt.best_sellers_list(
    date = datetime.datetime(2019, 1, 1),
    name = "hardcover-fiction"
)

nyt.movie_reviews(
    keyword = "FBI",
    options = {
        "order": "by-opening-date"
    }
)

nyt.article_metadata(
    url = "https://www.nytimes.com/2019/10/20/world/middleeast/erdogan-turkey-nuclear-weapons-trump.html"
)

## Remove tests for tags because the API doesnt work.
try:
    nyt.tag_query(
        "Pentagon",
        max_results = 20
    )
except:
    print("There is still an error with the Times Tags, it appears to be server related")


nyt.archive_metadata(
    date = datetime.datetime(2019, 1, 1)
)

nyt.article_search(
    query = "Trump",
    results = 20,
    dates = {
        "begin": datetime.datetime(2019, 1, 1),
        "end": datetime.datetime(2019, 2, 1)
    },
    options = {
        "sort": "oldest"
    }
)

end = datetime.datetime.now()
print(end - begin)