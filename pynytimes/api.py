"""The wrapper is here"""
import datetime
import math
import time
import warnings

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Import version from __init__
from . import __version__

# Define all URLs that are needed
BASE_URL = "api.nytimes.com"
BASE_TOP_STORIES = BASE_URL + "/svc/topstories/v2/"
BASE_MOST_POPULAR = BASE_URL + "/svc/mostpopular/v2/"
BASE_BOOKS = BASE_URL + "/svc/books/v3/"
BASE_MOVIE_REVIEWS = BASE_URL + "/svc/movies/v2/reviews/search.json"
BASE_META_DATA = BASE_URL + "/svc/news/v3/content.json"
BASE_TAGS = BASE_URL + "/svc/suggest/v1/timestags.json"
BASE_ARCHIVE_METADATA = BASE_URL + "/svc/archive/v1/"
BASE_ARTICLE_SEARCH = BASE_URL + "/svc/search/v2/articlesearch.json"
BASE_LATEST_ARTICLES = BASE_URL + "/svc/news/v3/content/"
BASE_SECTION_LIST = BASE_URL + "/svc/news/v3/content/section-list.json"
BASE_BOOK_REVIEWS = BASE_BOOKS + "reviews.json"
BASE_BEST_SELLERS_LISTS = BASE_BOOKS + "lists/names.json"
BASE_BEST_SELLERS_LIST = BASE_BOOKS + "lists/"

class NYTAPI:
    """This class interacts with the Python code, it primarily blocks wrong user input"""
    def __init__(self, key=None, https=True, session = requests.Session()):
        self.key = key
        
        # Add session to class so connection can be reused
        self.session = session

        # Define protocol to be used
        if https:
            self.protocol = "https://"
        else:
            self.protocol = "http://"

        # Set strategy to prevent HTTP 429 (Too Many Requests) errors
        backoff_strategy = Retry(
            total = 10,
            backoff_factor = 1,
            status_forcelist = [429, 509]
        )

        adapter = HTTPAdapter(
            max_retries = backoff_strategy
        )

        self.session.mount(self.protocol + "api.nytimes.com/", adapter)

        # Set header to show that this wrapper is used
        self.session.headers.update({"User-Agent": "pynytimes/" + __version__})

        if self.key is None:
            raise Exception("API key is not set, get an API-key from https://developer.nytimes.com.")

    def load_data(self, url, options=None, location=None):
        """This function loads the data for the wrapper for most API use cases"""
        # Set API key in query parameters
        params = { "api-key": self.key }

        # Add options to query parameters
        if options is not None:
            params.update(options)

        # Load the data from the API, raise error if there's an invalid status code
        res = self.session.get(url, params=params, timeout=(4, 10))
        res.raise_for_status()

        # Get the data from the usual results location
        if location is None:
            results = res.json().get("results")

        # Sometimes the results are in a different location, this location can be defined in a list
        # Load the data from that location
        else:
            results = res.json()
            for loc in location:
                results = results.get(loc)

        return results

    def top_stories(self, section=None):
        """Load the top stories"""
        # Set default section
        if section is None:
            section = "home"

        # Set the URL the data can be loaded from, and load the data
        url = self.protocol + BASE_TOP_STORIES + section + ".json"
        return self.load_data(url)

    def most_viewed(self, days=None):
        """Load most viewed articles"""
        # Set amount of days for top stories
        days_options = [1, 7, 30]
        if days is None:
            days = 1

        # Raise an Exception if number of days is invalid
        if days not in days_options:
            raise Exception("You can only select 1, 7 or 30 days")

        # Load the data
        url = self.protocol + BASE_MOST_POPULAR + "viewed/" + str(days) + ".json"
        return self.load_data(url)

    def most_shared(self, days = 1, method=None):
        """Load most shared articles"""
        # Check if options are valid
        method_options = [None, "email", "facebook"]
        days_options = [1, 7, 30]

        if method not in method_options:
            raise Exception("Shared option does not exist")

        if days not in days_options:
            raise Exception("You can only select 1, 7 or 30 days")

        # Set URL of data that needs to be loaded
        url = self.protocol

        if method is None:
            url += BASE_MOST_POPULAR + "shared/" + str(days) + ".json"
        elif method == "email":
            url += BASE_MOST_POPULAR + "emailed/" + str(days) + ".json"
        else:
            url += BASE_MOST_POPULAR + "shared/" + str(days) + "/" + method + ".json"
        
        # Load and return the data
        return self.load_data(url)

    def book_reviews(self, author=None, isbn=None, title=None):
        """Load book reviews"""
        # Check if request is valid
        if author and isbn and title is None:
            raise Exception("Not all fields in reviews can be empty")

        if int(isbn is not None) + int(title is not None) + int(author is not None) != 1:
            raise Exception("You can only define one of the following: ISBN, author or title.")

        # Set request options params
        options = {}
        if author is not None:
            options["author"] = author

        elif isbn is not None:
            options["isbn"] = str(isbn)

        elif title is not None:
            options["title"] = title

        # Set URL, load and return data
        url = self.protocol + BASE_BOOK_REVIEWS
        return self.load_data(url, options=options)

    def best_sellers_lists(self):
        """Load all the best seller lists"""
        # Set URL, load and return data
        url = self.protocol + BASE_BEST_SELLERS_LISTS
        return self.load_data(url)

    def best_sellers_list(self, date=None, name=None):
        """Load a best seller list"""
        # Set valid date
        if date is None:
            _date = "current"

        # Raise error if date is not a datetime.datetime object
        elif not isinstance(date, datetime.datetime):
            raise Exception("Date has to be a datetime object")

        # Set date if defined
        else:
            _date = date.strftime("%Y-%m-%d")

        # Set best seller list if not defined
        if name is None:
            name = "combined-print-and-e-book-fiction"

        # Set URL and include data
        url = self.protocol + BASE_BEST_SELLERS_LIST + _date + "/" + name + ".json"
        
        # Set location in JSON of results, load and return data
        location = ["results", "books"]
        return self.load_data(url, location=location)

    def movie_reviews(self, keyword=None, options=None, dates=None):
        """Load movie reviews"""
        # Set options and dates if not defined
        if options is None:
            options = {}

        if dates is None:
            dates = {}

        if options.get("max_results") is None:
            options["max_results"] = 20

        # Set request options if defined
        options["opening_date_start"] = dates.get("opening_date_start")
        options["opening_date_end"] = dates.get("opening_date_end")
        options["publication_date_start"] = dates.get("publication_date_start")
        options["publication_date_end"] = dates.get("publication_date_end")

        # Raise error if invalid option
        if options.get("order") not in [None, "by-opening-date", "by-publication-date", "by-title"]:
            raise Exception("Order is not a valid option")

        # Define a date if neccecary and convert all data to valid data for API request
        if options.get("opening_date_end") is not None \
        and options.get("opening_date_start") is None:
            options["opening_date_start"] = datetime.datetime(1900, 1, 1)

        if options.get("publication_date_end") is not None \
        and options.get("opening_date_start") is None:
            options["opening_date_start"] = datetime.datetime(1900, 1, 1)

        _opening_dates = None
        _publication_dates = None
        _critics_pick = None

        if options.get("opening_date_start") is not None:
            _opening_dates = options.get("opening_date_start").strftime("%Y-%m-%d") + ";"

        if options.get("opening_date_end") is not None:
            _opening_dates += options.get("opening_date_end").strftime("%Y-%m-%d")

        if options.get("publication_date_start") is not None:
            _publication_dates = options.get("opening_date_start").strftime("%Y-%m-%d") + ";"

        if options.get("publication_date_end") is not None:
            _publication_dates += options.get("opening_date_end").strftime("%Y-%m-%d")

        if options.get("critics_pick") is True:
            _critics_pick = "Y"

        # Load data from API, this doesn't uses the load_data function because it works slightly differently

        # Set API key in query params
        params = {"api-key": self.key}

        # Set keyword if defined
        if keyword is not None:
            params["query"] = keyword

        # Set API request params if defined
        params["critics-pick"] = options.get("critics")
        params["reviewer"] = options.get("reviewer")
        params["order"] = options.get("order")
        params["opening-date"] = options.get("opening")
        params["publication-date"] = options.get("publication")

        # Set URL request data
        url = self.protocol + BASE_MOVIE_REVIEWS

        # Set results list
        results = []

        # Keep loading data until amount of results is received
        for i in range(math.ceil(options["max_results"]/20)):
            # Set offset for second request
            offset = i*20
            params["offset"] = str(offset)

            # Load the data from the API and raise if there's an Error
            res = self.session.get(url, params=params, timeout=(4, 10))
            res.raise_for_status()

            # Parse results and append them to the results list
            res_parsed = res.json()
            results += res_parsed.get("results")

            # Quit loading more data if no more data is available
            if res_parsed.get("has_more") is False:
                break

        # Return the results
        return results

    def article_metadata(self, url):
        """Load the metadata from an article"""
        # Set metadata in requests params and define URL
        options = { "url": url }
        url = self.protocol + BASE_META_DATA

        # Load and return the data
        return self.load_data(url, options=options)

    def section_list(self):
        """Load all sections"""
        # Set URL, load and return the data
        url = self.protocol + BASE_SECTION_LIST
        return self.load_data(url)

    def latest_articles(self, source = "all", section = "all"):
        """Load the latest articles"""
        # Check if sections options is valid
        source_options = ["all", "nyt", "inyt"]

        if source not in source_options:
            raise Exception("Source is not a valid option")

        # Set URL, load and return data
        url = self.protocol + BASE_LATEST_ARTICLES + source + "/" + section + ".json"
        return self.load_data(url)

    def tag_query(self, query, filter_option=None, filter_options=None, max_results=None):
        """Load TimesTags, currently the API seems to be broken"""
        # Add filter options
        _filter_options = ""
        if filter_options is not None:
            for filter_opt in filter_options:
                if _filter_options is not None:
                    _filter_options += ","

                _filter_options += filter_opt

        elif filter_option is not None:
            _filter_options = filter_option

        # Add options to request params
        options = {
            "query": query,
            "filter": _filter_options
        }

        # Define amount of results wanted
        if max_results is not None:
            options["max"] = str(max_results)

        # Set URL, load and return data
        url = self.protocol + BASE_TAGS
        return self.load_data(url, options=options, location=[])[1]

    def archive_metadata(self, date):
        """Load all the metadata from one month"""
        # Raise Error if date is not defined
        if not isinstance(date, datetime.datetime):
            raise Exception("Date has to be datetime")

        # Get date as is needed in request
        _date = date.strftime("%Y/%-m")

        # Set URL, load and return data
        url = self.protocol + BASE_ARCHIVE_METADATA + _date + ".json"
        return self.load_data(url, location=["response", "docs"])

    @staticmethod
    def _article_search_search_options_helper(options):
        """"Help to create all fq queries"""
        # Get options already defined in fq (filter query)
        fq = options.get("fq")

        # Set query options that are currently supported
        current_filter_support = ["source", "news_desk", "section_name", "glocation", "type_of_material"]

        # Run for every filter
        for _filter in current_filter_support:
            # Get data for filter if it's not defined continue to next filter
            values = options.get(_filter)
            if values is None:
                continue

            # Check if filter query is already defined. If it is then add
            # " AND " to the query, otherwise create fq
            if isinstance(fq, str):
                fq += " AND "
            else:
                fq = ""

            # Add filter
            fq += _filter + ":("

            # Add all the data in the list to the filter
            for i, value in enumerate(values):
                fq += "\""
                fq += value
                fq += "\""

                if i < len(values) - 1:
                    fq += " "

            fq += ")"

            # Remove the filter from options
            del options[_filter]

        # If filter query was defined set fq
        if fq is not None:
            options["fq"] = fq
        
        # Return the options
        return options

    def article_search(self, query=None, dates=None, options=None, results=None):
        """Load articles from search"""
        # Set options and dates if undefined
        if options is None:
            options = {}

        if dates is None:
            dates = {}

        # Get dates if defined
        begin_date = dates.get("begin")
        end_date = dates.get("end")

        # Resolve filter options into fq
        options = self._article_search_search_options_helper(options)

        # Get and check if sort option is valid
        sort = options.get("sort")

        if sort not in [None, "newest", "oldest", "relevance"]:
            raise Exception("Sort option is not valid")

        # Set dates
        _begin_date = None
        _end_date = None

        # Show default amount of results if undefined
        if results is None:
            results = 10

        # Show warnings when a lot of results are requested
        if results >= 100:
            warnings.warn(
                "Asking for a lot of results, because of rate limits it can take a while."
            )

        # Set maximum amount of results
        if results >= 2010:
            results = 2010
            warnings.warn(
                "Asking for more results then the API can provide, loading maximum results."
            )

        # Raise error if dates aren't datetime.datetime objects
        if begin_date is not None:
            if not isinstance(begin_date, datetime.datetime):
                raise Exception("Begin date has to be datetime")

            _begin_date = begin_date.strftime("%Y%m%d")

        if end_date is not None:
            if not isinstance(end_date, datetime.datetime):
                raise Exception("End date has to be datetime")

            _end_date = end_date.strftime("%Y%m%d")

        # Set query if defined
        if query is not None:
            options["q"] = query

        # Set options params
        options["begin_date"] = _begin_date
        options["end_date"] = _end_date

        # Set params is options and set API key in params
        params = options
        params["api-key"] = self.key

        # Set url to load data from
        url = self.protocol + BASE_ARTICLE_SEARCH

        # Set result list and add request as much data as needed
        result = []
        for i in range(math.ceil(results/10)):
            # Set page
            params["page"] = str(i)

            # Load data and raise error if there's and error status
            res = self.session.get(url, params=params)
            res.raise_for_status()

            # Parse results and append them to results list
            result += res.json().get("response").get("docs")

            # Stop loading if all responses are already loaded
            if res.json().get("response").get("meta").get("hits") <= i*10:
                break

        # Return results
        return result
