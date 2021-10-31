from pynytimes import NYTAPI

# Make sure to turn parse dates on so that the dates
# are parsed into datetime.datetime or datetime.date objects
nyt = NYTAPI("API Key", parse_dates=True)

# Get top stories
top_stories = nyt.top_stories()

# Optionally you can also define a section
# Valid options for sections can be found in README
top_stories_science = nyt.top_stories(section="science")
