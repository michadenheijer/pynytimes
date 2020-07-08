"""The wrapper is here"""
import datetime
import math
import time
import warnings

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from . import __version__

BASE_TOP_STORIES = "api.nytimes.com/svc/topstories/v2/"
BASE_MOST_POPULAR = "api.nytimes.com/svc/mostpopular/v2/"
BASE_BOOKS = "api.nytimes.com/svc/books/v3/"
BASE_MOVIE_REVIEWS = "api.nytimes.com/svc/movies/v2/reviews/search.json"
BASE_META_DATA = "api.nytimes.com/svc/news/v3/content.json"
BASE_TAGS = "api.nytimes.com/svc/suggest/v1/timestags.json"
BASE_ARCHIVE_METADATA = "api.nytimes.com/svc/archive/v1/"
BASE_ARTICLE_SEARCH = "api.nytimes.com/svc/search/v2/articlesearch.json"
BASE_BOOK_REVIEWS = BASE_BOOKS + "reviews.json"
BASE_BEST_SELLERS_LISTS = BASE_BOOKS + "lists/names.json"
BASE_BEST_SELLERS_LIST = BASE_BOOKS + "lists/"

class NYTAPI:
    """This class interacts with the Python code, it primarily blocks wrong user input"""
    def __init__(self, key=None, https=True, session = requests.Session()):
        self.key = key
        self.session = session
        
        if https:
            self.protocol = "https://"
        else:
            self.protocol = "http://"

        backoff_strategy = Retry(
            total = 10,
            backoff_factor = 1,
            status_forcelist = [429, 509]
        )

        server_error_strategy = Retry(
            total = 2,
            backoff_factor = 1,
            status_forcelist = [500, 502, 503, 504]
        )

        self.session.mount(self.protocol + "api.nytimes.com/", HTTPAdapter(max_retries = backoff_strategy))
        self.session.mount(self.protocol + "api.nytimes.com/", HTTPAdapter(max_retries = server_error_strategy))

        self.session.headers.update({"User-Agent": "pynytimes/" + __version__})

        if self.key is None:
            raise Exception("No API key")

    def load_data(self, url, options=None, location=None):
        """This function loads the data for the wrapper for most API use cases"""
        params = { "api-key": self.key }

        if options is not None:
            params.update(options)

        res = self.session.get(url, params=params, timeout=(4, 10))
        res.raise_for_status()

        if location is None:
            results = res.json().get("results")

        else:
            results = res.json()
            for loc in location:
                results = results.get(loc)

        return results

    def top_stories(self, section=None):
        """Load the top stories"""
        if section is None:
            section = "home"

        url = self.protocol + BASE_TOP_STORIES + section + ".json"
        return self.load_data(url)

    def most_viewed(self, days=None):
        """Load most viewed articles"""
        days_options = [1, 7, 30]
        if days is None:
            days = 1

        if days not in days_options:
            raise Exception("You can only select 1, 7 or 30 days")

        url = self.protocol + BASE_MOST_POPULAR + "viewed/" + str(days) + ".json"
        return self.load_data(url)

    def most_shared(self, days=1, method=None):
        """Load most shared articles"""
        method_options = [None, "email", "facebook"]
        days_options = [1, 7, 30]

        if method not in method_options:
            raise Exception("Shared option does not exist")

        if days not in days_options:
            raise Exception("You can only select 1, 7 or 30 days")

        url = self.protocol

        if method is None:
            url += BASE_MOST_POPULAR + "shared/" + str(days) + ".json"
        elif method == "email":
            url += BASE_MOST_POPULAR + "emailed/" + str(days) + ".json"
        else:
            url += BASE_MOST_POPULAR + "shared/" + str(days) + "/" + method + ".json"
        
        return self.load_data(url)

    def book_reviews(self, author=None, isbn=None, title=None):
        """Load book reviews"""
        if author and isbn and title is None:
            raise Exception("Not all fields in reviews can be empty")

        if int(isbn is not None) + int(title is not None) + int(author is not None) != 1:
            raise Exception("You can only define one of the following: ISBN, author or title.")

        options = {}
        if author is not None:
            options["author"] = author

        elif isbn is not None:
            options["isbn"] = str(isbn)

        elif title is not None:
            options["title"] = title

        url = self.protocol + BASE_BOOK_REVIEWS
        return self.load_data(url, options=options)

    def best_sellers_lists(self):
        """Load all the best seller lists"""
        url = self.protocol + BASE_BEST_SELLERS_LISTS
        return self.load_data(url)

    def best_sellers_list(self, date=None, name=None):
        """Load a best seller list"""
        if date is None:
            _date = "current"

        elif not isinstance(date, datetime.datetime):
            raise Exception("Date has to be a datetime object")

        else:
            _date = date.strftime("%Y-%m-%d")

        if name is None:
            name = "combined-print-and-e-book-fiction"

        url = self.protocol + BASE_BEST_SELLERS_LIST + _date + "/" + name + ".json"
        location = ["results", "books"]
        return self.load_data(url, location=location)

    def movie_reviews(self, keyword=None, options=None, dates=None):
        """Load movie reviews"""
        if options is None:
            options = {}

        if dates is None:
            dates = {}

        if options.get("max_results") is None:
            options["max_results"] = 20
            
        options["opening_date_start"] = dates.get("opening_date_start")
        options["opening_date_end"] = dates.get("opening_date_end")
        options["publication_date_start"] = dates.get("publication_date_start")
        options["publication_date_end"] = dates.get("publication_date_end")

        if options.get("order") not in [None, "by-opening-date", "by-publication-date", "by-title"]:
            raise Exception("Order is not a valid option")

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

        params = {"api-key": self.key}

        if keyword is not None:
            params["query"] = keyword

        params["critics-pick"] = options.get("critics")
        params["reviewer"] = options.get("reviewer")
        params["order"] = options.get("order")
        params["opening-date"] = options.get("opening")
        params["publication-date"] = options.get("publication")

        url = self.protocol + BASE_MOVIE_REVIEWS

        results = []

        for i in range(math.ceil(options.max_results/20)):
            offset = i*20
            params["offset"] = str(offset)
            res = self.session.get(url, params=params, timeout=(4, 10))
            res.raise_for_status()
            res_parsed = res.json()
            results += res_parsed.get("results")

            if res_parsed.get("has_more") is False:
                break

        return results

    def article_metadata(self, url):
        """Load the metadata from an article"""
        options = { "url": url }
        url = self.protocol + BASE_META_DATA

        return self.load_data(url, options=options)

    def tag_query(self, query, filter_option=None, filter_options=None, max_results=None):
        """Load TimesTags"""
        _filter_options = ""
        if filter_options is not None:
            for filter_opt in filter_options:
                if _filter_options is not None:
                    _filter_options += ","

                _filter_options += filter_opt

        elif filter_option is not None:
            _filter_options = filter_option

        options = {
            "query": query,
            "filter": filter_options
        }

        if max_results is not None:
            options["max"] = str(max_results)

        url = self.protocol + BASE_TAGS

        return self.load_data(url, options=options, location=[])[1]

    def archive_metadata(self, date):
        """Load all the metadata from one month"""
        if not isinstance(date, datetime.datetime):
            raise Exception("Date has to be datetime")

        _date = date.strftime("%Y/%-m")

        url = self.protocol + BASE_ARCHIVE_METADATA + _date + ".json"
        return self.load_data(url, location=["response", "docs"])

    def article_search(self, query=None, dates=None, options=None, results=None):
        """Load articles from search"""
        if options is None:
            options = {}

        if dates is None:
            dates = {}

        begin_date = dates.get("begin")
        end_date = dates.get("end")

        sources = options.get("source")

        if sources is not None:
            _sources = "source:("

            for i, source in enumerate(sources):
                _sources += "\""
                _sources += source
                _sources += "\""

                if i < len(sources) - 1:
                    _sources += " "

            _sources += ")"

        _begin_date = None
        _end_date = None

        if results is None:
            results = 10

        if results >= 100:
            warnings.warn(
                "Asking for a lot of results, because of rate limits it can take a while."
            )

        if results >= 2010:
            results = 2010
            warnings.warn(
                "Asking for more results then the API can provide, loading maximum results."
            )

        if begin_date is not None:
            if not isinstance(begin_date, datetime.datetime):
                raise Exception("Begin date has to be datetime")

            _begin_date = begin_date.strftime("%Y%m%d")

        if end_date is not None:
            if not isinstance(end_date, datetime.datetime):
                raise Exception("End date has to be datetime")

            _end_date = end_date.strftime("%Y%m%d")

        if query is not None:
            options["q"] = query

        options["begin_date"] = _begin_date
        options["end_date"] = _end_date

        params = options
        params["api-key"] = self.key

        url = self.protocol + BASE_ARTICLE_SEARCH

        result = []
        for i in range(math.ceil(results/10)):
            params["page"] = str(i)

            res = self.session.get(url, params=params)
            res.raise_for_status()

            result += res.json().get("response").get("docs")

            if res.json().get("response").get("meta").get("hits") <= i*10:
                break


        return result
