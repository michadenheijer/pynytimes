from datetime import date, datetime
from pynytimes import NYTAPI

# Make sure to set parse dates to True so that the dates
# are parsed into datetime.datetime or datetime.date objects
nyt = NYTAPI(
    key="Your API Key",  # Get your API Key at https://developer.nytimes.com
    parse_dates=True,
)

# Search articles about President Biden
biden = nyt.article_search("biden")

# You can optionally define the dates between which you want the articles to be
biden_january = nyt.article_search(
    query="biden", dates={"begin": date(2021, 1, 1), "end": date(2021, 1, 31)}
)

# Optionally you can also define
biden = nyt.article_search(
    "biden",
)
