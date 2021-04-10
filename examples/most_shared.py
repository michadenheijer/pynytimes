from pynytimes import NYTAPI

# Make sure to set parse dates to True so that the dates
# are parsed into datetime.datetime or datetime.date objects
nyt = NYTAPI(
    key="Your API Key",  # Get your API Key at https://developer.nytimes.com
    parse_dates=True,
)

# Get most shared articles of today
most_shared = nyt.most_shared()

# Optionally you can also define the timeframe
# Valid options are 1, 7, 30
most_shared_last_week = nyt.most_shared(days=7)
most_shared_last_month = nyt.most_shared(days=30)

# You can also define the method of sharing.
# Options are: email (default) or facebook.
most_shared_email = nyt.most_shared(method="email")
most_shared_facebook = nyt.most_shared(method="facebook")

# These options can also be mixed and matched
# So the most shared articles of last month on facebook are
most_shared_last_month_facebook = nyt.most_shared(days=30, method="facebook")
