from pynytimes import NYTAPI

# Make sure to turn parse dates on so that the dates
# are parsed into datetime.datetime or datetime.date objects
nyt = NYTAPI("API Key", parse_dates=True)

# Get the most viewed articles of today
most_viewed = nyt.most_viewed()

# Optionally you can also define the time period of the most
# viewed articles
most_viewed_last_week = nyt.most_viewed(days=7)  # Valid options are 1, 7 or 30
most_viewed_last_month = nyt.most_viewed(days=30)
