"""The wrapper is here"""
# Import typings dependencies
from __future__ import annotations
from typing import Any, Union, Optional

# Import standard Python dependencies
import warnings
import datetime
import math
import re

# Import other dependencies
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Try importing orjson, if not available just ignore
try:
    import orjson
except ImportError:
    orjson = None

# Import version from __init__
from .__version__ import __version__

# Define all URLs that are needed
BASE_URL = "api.nytimes.com"
BASE_TOP_STORIES = BASE_URL + "/svc/topstories/v2/"
BASE_MOST_POPULAR = BASE_URL + "/svc/mostpopular/v2/"
BASE_BOOKS = BASE_URL + "/svc/books/v3/"
BASE_MOVIE_REVIEWS = BASE_URL + "/svc/movies/v2/reviews/search.json"
BASE_META_DATA = BASE_URL + "/svc/news/v3/content.json"
BASE_TAGS = BASE_URL + "/svc/semantic/v2/concept/suggest"
BASE_ARCHIVE_METADATA = BASE_URL + "/svc/archive/v1/"
BASE_ARTICLE_SEARCH = BASE_URL + "/svc/search/v2/articlesearch.json"
BASE_LATEST_ARTICLES = BASE_URL + "/svc/news/v3/content/"
BASE_SECTION_LIST = BASE_URL + "/svc/news/v3/content/section-list.json"
BASE_BOOK_REVIEWS = BASE_BOOKS + "reviews.json"
BASE_BEST_SELLERS_LISTS = BASE_BOOKS + "lists/names.json"
BASE_BEST_SELLERS_LIST = BASE_BOOKS + "lists/"


class NYTAPI:
    """New York Times API Class. Interacts with user."""

    # pylint: disable=too-many-arguments

    def __init__(
        self,
        key: Optional[str] = None,
        https: bool = True,
        session: Optional[Session] = None,
        backoff: bool = True,
        user_agent: Optional[str] = None,
        parse_dates: bool = False,
    ) -> NYTAPI:
        # Raise Error if API key is not given, or wrong type
        if key is None:
            raise ValueError(
                "API key is not set, get an API-key from https://developer.nytimes.com."
            )

        if not isinstance(key, str):
            raise TypeError("API key needs to be str")

        # Set API key
        self.key: str = key

        # Check if session is Session, add session to class so connection can be reused
        if session is None:
            session = Session()

        if not isinstance(session, Session):
            raise TypeError("Session needs to be a Session object")

        self.session = session

        # Check if parse_dates is bool, if correct set parse_dates
        if not isinstance(parse_dates, bool):
            raise TypeError("parse_dates needs to be bool")

        self.parse_dates = parse_dates

        # Define protocol to be used
        if not isinstance(https, bool):
            raise TypeError("https needs to be bool")

        if https:
            self.protocol = "https://"
        else:
            self.protocol = "http://"

        # Set strategy to prevent HTTP 429 (Too Many Requests) errors
        if not isinstance(backoff, bool):
            raise TypeError("backoff needs to be bool")

        if backoff:
            backoff_strategy = Retry(
                total=10, backoff_factor=1, status_forcelist=[429, 509]
            )

            adapter = HTTPAdapter(max_retries=backoff_strategy)

            self.session.mount(self.protocol + "api.nytimes.com/", adapter)

        # Set header to show that this wrapper is used
        if user_agent is None:
            user_agent = "pynytimes/" + __version__

        if not isinstance(user_agent, str):
            raise TypeError("user_agent needs to be str")

        self.session.headers.update({"User-Agent": user_agent})

    def __enter__(self) -> NYTAPI:
        return self

    def _load_data(
        self,
        url: str,
        options: Optional[dict[str, Any]] = None,
        location: Optional[list] = None,
    ) -> list[dict[str, Any]]:
        """This function loads the data for the wrapper for most API use cases"""
        # Set API key in query parameters
        params = {"api-key": self.key}

        # Add options to query parameters
        if options is not None:
            params.update(options)

        # Load the data from the API, raise error if there's an invalid status
        # code
        timeout = (4, 10)
        res = self.session.get(self.protocol + url, params=params, timeout=timeout)

        if res.status_code == 400:
            raise ValueError("Error 400: Invalid input")

        if res.status_code == 401:
            raise ValueError("Error 401: Invalid API Key")

        if res.status_code == 403:
            raise RuntimeError("Error 403: You don't have access to this page")

        if res.status_code == 404:
            raise RuntimeError("Error 404: This page does not exist")

        res.raise_for_status()

        if orjson is None:
            parsed_res: dict[str, Any] = res.json()
        else:
            parsed_res: dict[str, Any] = orjson.loads(res.content)

        # Get the data from the usual results location
        results: dict[str, Any]
        if location is None:
            results = parsed_res.get("results")

        # Sometimes the results are in a different location, this location can be defined in a list
        # Load the data from that location
        else:
            results = parsed_res
            for loc in location:
                results = results.get(loc)

        return results

    @staticmethod
    def _parse_date(
        date_string: str, date_type: str
    ) -> Union[datetime.datetime, datetime.date, None]:
        """Parse the date into datetime.datetime object"""
        # If date_string is None return None
        if date_string is None:
            return None

        # Parse rfc3339 dates from str
        if date_type == "rfc3339":
            # This if statement is to make it compatible with Python 3.6
            if date_string[-3] == ":":
                date_string = date_string[:-3] + date_string[-2:]

            return datetime.datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S%z")

        # Parse date only strings
        if date_type == "date-only":
            if re.match(r"^(\d){4}-00-00$", date_string):
                return datetime.datetime.strptime(date_string, "%Y-00-00").date()

            return datetime.datetime.strptime(date_string, "%Y-%m-%d").date()

        if date_type == "date-time":
            return datetime.datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")

        return None

    def _parse_dates(
        self, articles: list, date_type: str, locations: Optional[list] = None
    ) -> list[dict[str, Any]]:
        """Parse dates to datetime"""
        # Create list locations is None
        if locations is None:
            locations = []

        # Don't parse if parse_dates is False
        if self.parse_dates is False:
            return articles

        # Create parsed_articles list
        parsed_articles = []

        # For every article parse date_string into datetime.datetime
        for article in articles:
            parsed_article = article
            for location in locations:
                parsed_article[location] = self._parse_date(
                    parsed_article[location], date_type
                )
            parsed_articles.append(article)

        return parsed_articles

    def top_stories(self, section: str = "home") -> list[dict[str, Any]]:
        """Load the top stories"""
        # Raise error if section is not a str
        if not isinstance(section, str):
            raise TypeError("Section can only be a str")

        # Set the URL the data can be loaded from, and load the data
        url = BASE_TOP_STORIES + section + ".json"

        try:
            result = self._load_data(url)

        # If 404 error throw invalid section name error
        except RuntimeError:
            raise ValueError("Invalid section name")

        # Parse dates from string to datetime.datetime
        date_locations = ["updated_date", "created_date", "published_date"]
        parsed_result = self._parse_dates(result, "rfc3339", date_locations)

        return parsed_result

    def most_viewed(self, days: int = 1) -> list[dict[str, Any]]:
        """Load most viewed articles"""
        days_options = [1, 7, 30]

        # Raise an Exception if days is not a int
        if not isinstance(days, int):
            raise TypeError("You can only enter an int")

        # Raise an Exception if number of days is invalid
        if days not in days_options:
            raise ValueError("You can only select 1, 7 or 30 days")

        # Load the data
        url = BASE_MOST_POPULAR + "viewed/" + str(days) + ".json"
        result = self._load_data(url)

        parsed_date_result = self._parse_dates(result, "date-only", ["published_date"])
        parsed_result = self._parse_dates(parsed_date_result, "date-time", ["updated"])

        return parsed_result

    def most_shared(self, days: int = 1, method: str = "email") -> list[dict[str, Any]]:
        """Load most shared articles"""
        # Check if options are valid
        method_options = ["email", "facebook"]
        days_options = [1, 7, 30]

        # Raise error if method isn't a str
        if not isinstance(method, str):
            raise TypeError("Method needs to be str")

        # Raise error if days isn't an int
        if not isinstance(days, int):
            raise TypeError("Days needs to be int")

        # Raise error if days, or method aren't in options
        if method not in method_options:
            raise ValueError("Shared option does not exist")

        if days not in days_options:
            raise ValueError("You can only select 1, 7 or 30 days")

        # Set URL of data that needs to be loaded
        url = BASE_MOST_POPULAR

        if method is None:
            url += "shared/" + str(days) + ".json"
        elif method == "email":
            url += "emailed/" + str(days) + ".json"
        else:
            url += "shared/" + str(days) + "/" + method + ".json"

        # Load the data
        result = self._load_data(url)

        # Parse the date_strings into datetime.datetime
        parsed_date_result = self._parse_dates(result, "date-only", ["published_date"])
        parsed_result = self._parse_dates(parsed_date_result, "date-time", ["updated"])

        return parsed_result

    def book_reviews(
        self,
        author: Optional[str] = None,
        isbn: Union[str, int, None] = None,
        title: Optional[str] = None,
    ) -> list[dict[str, Any]]:
        """Load book reviews"""
        # Check if request is valid
        if author and isbn and title is None:
            raise ValueError("Not all fields in reviews can be empty")

        if (
            int(isbn is not None) + int(title is not None) + int(author is not None)
            != 1
        ):
            raise ValueError(
                "You can only define one of the following: ISBN, author or title."
            )

        # Set request options params and raise error if author is not a str,
        # isbn is not a str or int, or title is not a str
        options = {}
        if author is not None:
            if not isinstance(author, str):
                raise TypeError("Author needs to be str")
            options["author"] = author

        elif isbn is not None:
            if not isinstance(isbn, (int, str)):
                raise TypeError("ISBN needs to be int or str")
            options["isbn"] = str(isbn)

        elif title is not None:
            if not isinstance(title, str):
                raise TypeError("Title needs to be str")
            options["title"] = title

        # Set URL, load and return data
        url = BASE_BOOK_REVIEWS
        result = self._load_data(url, options=options)

        parsed_result = self._parse_dates(result, "date-only", ["publication_dt"])
        return parsed_result

    def best_sellers_lists(self) -> list[dict[str, Any]]:
        """Load all the best seller lists"""
        # Set URL, load and return data
        url = BASE_BEST_SELLERS_LISTS

        result = self._load_data(url)

        parsed_result = self._parse_dates(
            result, "date-only", ["oldest_published_date", "newest_published_date"]
        )
        return parsed_result

    def best_sellers_list(
        self,
        date: Union[datetime.date, datetime.datetime, None] = None,
        name: str = "combined-print-and-e-book-fiction",
    ) -> list[dict[str, Any]]:
        """Load a best seller list"""
        # Convert datetime.date into datetime.datetime
        if isinstance(date, datetime.date):
            date = datetime.datetime(date.year, date.month, date.day)

        # Set valid date
        if date is None:
            _date = "current"

        # Raise error if date is not a datetime.datetime object
        elif not isinstance(date, datetime.datetime):
            raise TypeError("Date has to be a datetime object")

        # Set date if defined
        else:
            _date = date.strftime("%Y-%m-%d")

        # Set URL and include data
        url = BASE_BEST_SELLERS_LIST + _date + "/" + name + ".json"

        # Set location in JSON of results, load and return data
        location = ["results", "books"]
        try:
            result = self._load_data(url, location=location)
        except RuntimeError:
            raise ValueError("Best sellers list name is invalid")

        return result

    def movie_reviews(
        self,
        keyword: Optional[str] = None,
        options: Optional[dict[str, Any]] = None,
        dates: Optional[dict[str, Union[datetime.date, datetime.datetime]]] = None,
    ) -> list[dict[str, Any]]:
        """Load movie reviews"""
        # Set options and dates if not defined
        if options is None:
            options = {}

        if dates is None:
            dates = {}

        # Raise error if keyword is not a string or NoneType
        if not isinstance(keyword, (str, type(None))):
            raise TypeError("Keyword needs to be str")

        # Raise error if options or date is not a dict
        if not isinstance(options, dict):
            raise TypeError("Options needs to be dict")

        if not isinstance(dates, dict):
            raise TypeError("Dates needs to be dict")

        # Raise error if dates in date is not a datetime.date or
        # datetime.datetime object
        for date in dates.items():
            if not isinstance(date[1], (datetime.datetime, datetime.date)):
                raise TypeError(
                    "Date items need to be datetime.date or datetime.datetime"
                )

            # Convert datetime.date to datetime.datetime
            if isinstance(date[1], datetime.date):
                dates[date[0]] = datetime.datetime(
                    date[1].year, date[1].month, date[1].day
                )

        if options.get("max_results") is None:
            options["max_results"] = 20

        # Set request options if defined
        options["opening_date_start"] = dates.get("opening_date_start")
        options["opening_date_end"] = dates.get("opening_date_end")
        options["publication_date_start"] = dates.get("publication_date_start")
        options["publication_date_end"] = dates.get("publication_date_end")

        # Raise error if invalid option
        if not isinstance(options.get("order"), (str, type(None))):
            raise TypeError("Order needs to be a string")

        order_options = [None, "by-opening-date", "by-publication-date", "by-title"]

        if options.get("order") not in order_options:
            raise ValueError("Order is not a valid option")

        # Define a date if neccecary and convert all data to valid data for API
        # request
        if (
            options.get("opening_date_end") is not None
            and options.get("opening_date_start") is None
        ):
            options["opening_date_start"] = datetime.datetime(1900, 1, 1)

        if (
            options.get("publication_date_end") is not None
            and options.get("opening_date_start") is None
        ):
            options["opening_date_start"] = datetime.datetime(1900, 1, 1)

        _opening_dates = None
        _publication_dates = None
        _critics_pick = None

        if options.get("opening_date_start") is not None:
            _opening_dates = options["opening_date_start"].strftime("%Y-%m-%d")
            _opening_dates += ";"

        if options.get("opening_date_end") is not None:
            _opening_dates += options["opening_date_end"].strftime("%Y-%m-%d")

        if options.get("publication_date_start") is not None:
            _publication_dates = options["opening_date_start"].strftime("%Y-%m-%d")
            _publication_dates += ";"

        if options.get("publication_date_end") is not None:
            _publication_dates += options["opening_date_end"].strftime("%Y-%m-%d")

        if options.get("critics_pick") is True:
            _critics_pick = "Y"
        elif not isinstance(options.get("critics_pick", False), bool):
            raise TypeError("Critics Pick needs to be a bool")

        # Set API key in query params
        params = {}

        # Set keyword if defined
        if keyword is not None:
            params["query"] = keyword

        # Set API request params if defined
        params["critics-pick"] = _critics_pick
        params["reviewer"] = options.get("reviewer")
        params["order"] = options.get("order")
        params["opening-date"] = _opening_dates
        params["publication-date"] = _publication_dates

        # Set URL request data
        url = BASE_MOVIE_REVIEWS

        # Set results list
        results = []

        # Keep loading data until amount of results is received
        for i in range(math.ceil(options["max_results"] / 20)):
            # Set offset for second request
            offset = i * 20
            params["offset"] = str(offset)

            # Load the data from the API and raise if there's an Error
            res = self._load_data(url, options=params, location=[])

            results += res.get("results")

            # Quit loading more data if no more data is available
            if res.get("has_more") is False:
                break

        # Parse and return the results
        parsed_date_results = self._parse_dates(
            results, "date-only", ["publication_date", "opening_date"]
        )
        parsed_results = self._parse_dates(
            parsed_date_results, "date-time", ["date_updated"]
        )

        return parsed_results

    def article_metadata(self, url: str) -> list[dict[str, Any]]:
        """Load the metadata from an article"""
        # Raise error if url is not an str
        if not isinstance(url, str):
            raise TypeError("URL needs to be str")

        # Set metadata in requests params and define URL
        options = {"url": url}
        url = BASE_META_DATA

        # Load, parse and return the data
        result = self._load_data(url, options=options)

        # Check if result is valid
        if result[0].get("published_date") == "0000-12-31T19:03:58-04:56":
            raise ValueError(
                "Invalid URL, the API cannot parse metadata from live articles"
            )

        date_locations = [
            "updated_date",
            "created_date",
            "published_date",
            "first_published_date",
        ]
        parsed_result = self._parse_dates(result, "rfc3339", date_locations)
        return parsed_result

    def section_list(self) -> list[dict[str, Any]]:
        """Load all sections"""
        # Set URL, load and return the data
        url = BASE_SECTION_LIST
        return self._load_data(url)

    def latest_articles(
        self, source: str = "all", section: str = "all"
    ) -> list[dict[str, Any]]:
        """Load the latest articles"""
        if not isinstance(source, str):
            raise TypeError("Source needs to be str")

        if not isinstance(section, str):
            raise TypeError("Section needs to be str")

        # Check if sections options is valid
        source_options = ["all", "nyt", "inyt"]

        if source not in source_options:
            raise ValueError("Source is not a valid option")

        # Set URL, load and return data
        url = BASE_LATEST_ARTICLES + source + "/" + section + ".json"
        try:
            result = self._load_data(url)
        except RuntimeError:
            raise ValueError("Section is not a valid option")

        date_locations = [
            "updated_date",
            "created_date",
            "published_date",
            "first_published_date",
        ]
        parsed_result = self._parse_dates(result, "rfc3339", date_locations)
        return parsed_result

    def tag_query(
        self,
        query: str,
        filter_option: Optional[dict[str, Any]] = None,
        filter_options: Optional[str] = None,
        max_results: Optional[int] = None,
    ) -> list[str]:
        """Load TimesTags"""
        # Raise error for TypeError
        if not isinstance(query, str):
            raise TypeError("Query needs to be str")

        if not isinstance(max_results, (type(None), int)):
            raise TypeError("Max results needs to be int")

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
        options = {"query": query, "filter": _filter_options}

        # Define amount of results wanted
        if max_results is not None:
            options["max"] = str(max_results)

        # Set URL, load and return data
        url = BASE_TAGS
        return self._load_data(url, options=options, location=[])[1]

    def archive_metadata(
        self, date: Union[datetime.datetime, datetime.date]
    ) -> list[dict[str, Any]]:
        """Load all the metadata from one month"""
        # Also accept datetime.date, convert it to datetime.datetime
        if isinstance(date, datetime.date):
            date = datetime.datetime(date.year, date.month, date.day)

        # Raise Error if date is not defined
        if not isinstance(date, datetime.datetime):
            raise TypeError("Date has to be datetime")

        # Get date as is needed in request
        year = date.year
        month = date.month
        _date = f"{year}/{month}"

        # Set URL, load and return data
        url = BASE_ARCHIVE_METADATA + _date + ".json"

        result = self._load_data(url, location=["response", "docs"])
        parsed_result = self._parse_dates(result, "rfc3339", ["pub_date"])
        return parsed_result

    @staticmethod
    def _article_search_search_options_helper(options: dict[str, Any]) -> dict:
        """ "Help to create all fq queries"""
        # pylint: disable=invalid-name
        # Get options already defined in fq (filter query)
        fq = options.get("fq")

        # Set query options that are currently supported
        current_filter_support = [
            "source",
            "news_desk",
            "section_name",
            "glocation",
            "type_of_material",
        ]

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
                fq += '"'
                fq += value
                fq += '"'

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

    def article_search(
        self,
        query: Optional[str] = None,
        dates: Optional[dict[str, Union[datetime.date, datetime.datetime]]] = None,
        options: Optional[dict[str, Any]] = None,
        results: int = 10,
    ) -> list[dict[str, Any]]:
        """Load articles from search"""
        # Set if None
        if dates is None:
            dates = {}

        if options is None:
            options = {}

        # Raise error if invalid parameters
        if not isinstance(query, (str, type(None))):
            raise TypeError("Query needs to be None or str")

        if not isinstance(dates, dict):
            raise TypeError("Dates needs to be a dict")

        if not isinstance(options, dict):
            raise TypeError("Options needs to be a dict")

        if not isinstance(results, (int, type(None))):
            raise TypeError("Results needs to be None or int")

        # Get dates if defined
        begin_date = dates.get("begin")
        end_date = dates.get("end")

        # Resolve filter options into fq
        options = self._article_search_search_options_helper(options)

        # Get and check if sort option is valid
        sort = options.get("sort")

        if sort not in [None, "newest", "oldest", "relevance"]:
            raise ValueError("Sort option is not valid")

        # Set dates
        _begin_date = None
        _end_date = None

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
            if isinstance(begin_date, datetime.date):
                begin_date = datetime.datetime(
                    begin_date.year, begin_date.month, begin_date.day
                )
            elif not isinstance(begin_date, datetime.datetime):
                raise TypeError(
                    "Begin date has to be datetime.datetime or datetime.date"
                )

            _begin_date = begin_date.strftime("%Y%m%d")

        if end_date is not None:
            if isinstance(end_date, datetime.date):
                end_date = datetime.datetime(
                    end_date.year, end_date.month, end_date.day
                )
            elif not isinstance(end_date, datetime.datetime):
                raise TypeError("End date has to be datetime.datetime or datetime.date")

            _end_date = end_date.strftime("%Y%m%d")

        # Set query if defined
        if query is not None:
            options["q"] = query

        # Set options params
        options["begin_date"] = _begin_date
        options["end_date"] = _end_date

        url = BASE_ARTICLE_SEARCH

        # Set result list and add request as much data as needed
        result = []
        for i in range(math.ceil(results / 10)):
            # Set page
            options["page"] = str(i)

            location = ["response"]
            # Load data and raise error if there's and error status
            res = self._load_data(url, options=options, location=location)

            # Parse results and append them to results list
            result += res.get("docs")

            # Stop loading if all responses are already loaded
            if res.get("meta").get("hits") <= i * 10:
                break

        # Parse and return results
        parsed_result = self._parse_dates(result, "rfc3339", ["pub_date"])
        return parsed_result

    # Allow the option to close the session
    def close(self) -> None:
        """Close session"""
        if self.session:
            self.session.close()

    # Close session before delete
    def __del__(self) -> None:
        """Close session on deletion"""
        self.close()

    def __exit__(self, *args) -> None:
        """Close session on exit"""
        self.close()
