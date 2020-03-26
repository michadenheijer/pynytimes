from pynytimes import NYTAPI

import datetime
import random
import time
import os

random_wait = random.randint(0, 60)
time.sleep(random_wait)

begin = datetime.datetime.now()

API_KEY = os.environ["NewYorkTimesAPIKey"]
nyt = NYTAPI(API_KEY)

nyt.top_stories(section="science")
nyt.most_viewed(days=30)
time.sleep(5)
nyt.most_shared(
    days = 30,
    method = "email"
)
nyt.book_reviews(
    author = "Michelle Obama"
)
time.sleep(5)
nyt.best_sellers_lists()
nyt.best_sellers_list(
    date = datetime.datetime(2019, 1, 1),
    name = "hardcover-fiction"
)
time.sleep(5)
nyt.movie_reviews(
    keyword = "FBI",
    options = {
        "order": "by-opening-date"
    }
)
nyt.article_metadata(
    url = "https://www.nytimes.com/2019/10/20/world/middleeast/erdogan-turkey-nuclear-weapons-trump.html"
)
time.sleep(5)
nyt.tag_query(
    "Pentagon",
    max_results = 20
)
nyt.archive_metadata(
    date = datetime.datetime(2019, 1, 1)
)
time.sleep(5)
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
