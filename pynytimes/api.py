"""Main function of the wrapper"""

# Import typings dependencies
from __future__ import annotations

# Import standard Python dependencies
import datetime
import warnings
import math
from typing import Any, Final, Literal, Optional, Union, TypedDict, cast

# Import other dependencies
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Import version from __init__
from .__version__ import __title__, __version__

# Import own dependencies
from .helpers import *

# Define all URLs that are needed
BASE_URL: Final = "api.nytimes.com/svc/"
BASE_TOP_STORIES: Final = BASE_URL + "topstories/v2/"
BASE_MOST_POPULAR: Final = BASE_URL + "mostpopular/v2/"
BASE_BOOKS: Final = BASE_URL + "books/v3/"
BASE_MOVIE_REVIEWS: Final = BASE_URL + "movies/v2/reviews/search.json"
BASE_META_DATA: Final = BASE_URL + "news/v3/content.json"
BASE_TAGS: Final = BASE_URL + "suggest/v1/timestags"
BASE_ARCHIVE_METADATA: Final = BASE_URL + "archive/v1/"
BASE_ARTICLE_SEARCH: Final = BASE_URL + "search/v2/articlesearch.json"
BASE_LATEST_ARTICLES: Final = BASE_URL + "news/v3/content/"
BASE_SECTION_LIST: Final = BASE_URL + "news/v3/content/section-list.json"
BASE_BOOK_REVIEWS: Final = BASE_BOOKS + "reviews.json"
BASE_BEST_SELLERS_LISTS: Final = BASE_BOOKS + "lists/names.json"
BASE_BEST_SELLERS_LIST: Final = BASE_BOOKS + "lists/"

# Define Requests variables
TIMEOUT: Final = (10, 30)
BACKOFF_FACTOR = 1
BACKOFF_MAX = 10
BACKOFF_JITTER = 0.5
RETRY_STATUS_CODES = [429, 509]
MAX_RETRIES = 10
RESULTS_MOVIE = 20
RESULTS_SEARCH = 10

# Set type hints
DateType = Union[datetime.date, datetime.datetime, None]
ArticleSearchOptions = TypedDict(
    "ArticleSearchOptions",
    {
        "sort": Literal["oldest", "newest", "relevance"],
        "sources": "list[str]",
        "news_desk": "list[str]",
        "type_of_material": "list[str]",
        "section_name": "list[str]",
        "subject": "list[str]",
        "body": "list[str]",
        "headline": "list[str]",
        "fq": "str",
    },
    total=False,
)
MovieReviewsOptions = TypedDict(
    "MovieReviewsOptions",
    {
        "order": Literal["by-title", "by-publication-date", "by-opening-date"],
        "reviewer": str,
        "critics_pick": bool,
    },
    total=False,
)


class NYTAPI:
    """
    New York Times API Class loads data from the NYT API.
    """

    key: str
    https: bool
    session: Session
    backoff: bool
    user_agent: str
    parse_dates: bool

    # pylint: disable=too-many-arguments

    def __init__(
        self,
        key: str,
        https: bool = True,
        session: Optional[Session] = None,
        backoff: bool = True,
        user_agent: Optional[str] = None,
        parse_dates: bool = False,
    ):
        """Creates the New York Times API class.

        Args:
            key (str): Your key to access the NYT developer API.
            Get your key at https://developer.nytimes.nl. Defaults to None.
            https (bool, optional): Optionally disable HTTPS, not advised.
            Defaults to True.
            session (Session, optional): Use your own Session object. Defaults to None.
            backoff (bool, optional): Optionally disable the automatic backoff,
            this is only advised if you implement your own. Defaults to True.
            user_agent (str, optional): Set your own user-agent. Defaults to None.
            parse_dates (bool, optional): Optionally parse all dates into datetime
            objects.
            It is advised to enable this. Defaults to False.
        """
        self.__set_key(key)
        self.__set_session(session)
        self.__set_parse_dates(parse_dates)
        self.__set_protocol(https)
        self.__set_backoff(backoff)
        self.__set_user_agent(user_agent)

    def __set_key(self, key: Optional[str]):
        """Set key of the class

        Args:
            key (str): The New York Times developer key

        Raises:
            ValueError: You have not set an API key, set one
            TypeError: Your API key is not a string
        """
        # Raise Error if API key is not given, or wrong type
        if key is None:
            raise ValueError(
                "API key is not set, get an API-key from "
                + "https://developer.nytimes.com."
            )

        if not isinstance(key, str):
            raise TypeError("API key needs to be str")

        # Set API key
        self.key: str = key

    def __set_session(self, session: Optional[Session]):
        # Check if session is Session, add session to class so connection
        # can be reused
        self._local_session = False
        if session is None:
            self._local_session = True
            session = Session()

        # FIXME maybe also support other types of requests compatible
        # Session instances
        if not isinstance(session, Session):
            raise TypeError("Session needs to be a Session object")

        self.session = session

    def __set_parse_dates(self, parse_dates: bool):
        # Check if parse_dates is bool, if correct set parse_dates
        if not isinstance(parse_dates, bool):
            raise TypeError("parse_dates needs to be bool")

        self.parse_dates = parse_dates

    def __set_protocol(self, https: bool):
        # Define protocol to be used
        if not isinstance(https, bool):
            raise TypeError("https needs to be bool")

        if https:
            self.protocol = "https://"
        else:
            self.protocol = "http://"

    def __set_backoff(self, backoff: bool):
        # Set strategy to prevent HTTP 429 (Too Many Requests) errors
        if not isinstance(backoff, bool):
            raise TypeError("backoff needs to be bool")

        if backoff:
            # Any to remove errors from type checker
            # FIXME maybe set this as a constant
            backoff_strategy = Retry(
                total=MAX_RETRIES,
                backoff_factor=BACKOFF_FACTOR,
                backoff_max=BACKOFF_MAX,
                status_forcelist=RETRY_STATUS_CODES,
                backoff_jitter=BACKOFF_JITTER,
            )

            adapter = HTTPAdapter(max_retries=backoff_strategy)

            self.session.mount(self.protocol + BASE_URL, adapter)

    def __set_user_agent(self, user_agent: Optional[str]):
        # Set header to show that this wrapper is used
        if user_agent is None:
            user_agent = f"{__title__}/{__version__}"

        if not isinstance(user_agent, str):
            raise TypeError("user_agent needs to be str")

        self.session.headers.update({"User-Agent": user_agent})

    def __enter__(self) -> NYTAPI:
        return self

    def __load_data(
        self,
        url: str,
        options: Optional[dict[str, Any]] = None,
        location: Optional[list[str]] = None,
    ) -> Union[list[dict[str, Any]], dict[str, Any]]:
        """This function loads the data for the wrapper for most API use cases"""
        # Set API key in query parameters
        params = {"api-key": self.key}

        # Add options to query parameters
        params.update(options or {})  # add empty list if None

        # Load the data from the API, raise error if there's an invalid status
        # code
        res = self.session.get(
            f"{self.protocol}{url}",
            params=params,
            timeout=TIMEOUT,
        )

        raise_for_status(res)
        parsed_res: dict[str, Any] = res.json()
        return get_from_location(parsed_res, location)

    def __parse_dates(
        self,
        articles: list[dict[str, str]],
        date_type: Literal["rfc3339", "date-only", "date-time"],
        locations: Optional[list] = None,
    ) -> list[dict[str, Any]]:
        """Parse dates to datetime"""
        # Don't parse if parse_dates is False
        return (
            parse_dates(articles, date_type, locations)
            if self.parse_dates
            else articles
        )

    def top_stories(self, section: str = "home") -> list[dict[str, Any]]:
        """Load Top Stories

        Args:
            section (str, optional): The section to load the top stories from.
            Defaults to "home".

        Raises:
            TypeError: Section can only be a string
            ValueError: A non-existant section is given

        Returns:
            list[dict[str, Any]]: Top stories metadata
        """
        # Raise error if section is not a str
        if not isinstance(section, str):
            raise TypeError("Section can only be a str")

        # Set the URL the data can be loaded from, and load the data
        url = f"{BASE_TOP_STORIES}{section}.json"

        try:
            result: list[dict[str, Any]] = self.__load_data(url)  # type:ignore
        # If 404 error throw invalid section name error
        except RuntimeError:
            raise ValueError("Invalid section name")

        # Parse dates from string to datetime.datetime
        # FIXME probably this should be a constant
        date_locations = ["updated_date", "created_date", "published_date"]
        parsed_result = self.__parse_dates(
            result, "rfc3339", date_locations
        )  # FIXME this could just be a direct return
        return parsed_result

    def most_viewed(self, days: Literal[1, 7, 30] = 1) -> list[dict[str, Any]]:
        """Get most viewed articles

        Args:
            days (Literal[1, 7, 30], optional): Select the period of which you
            want to get the most viewed articles. Defaults to 1.

        Returns:
            list[dict[str, Any]]: Most viewed article metadata
        """
        most_viewed_check_values(days)

        # Load the data
        url = f"{BASE_MOST_POPULAR}viewed/{days}.json"
        result: list[dict[str, Any]] = self.__load_data(url)  # type:ignore

        # Parse the dates in the results
        parsed_result = self.__parse_dates(
            self.__parse_dates(result, "date-only", ["published_date"]),
            "date-time",
            ["updated"],
        )

        return parsed_result

    def most_shared(
        self,
        days: Literal[1, 7, 30] = 1,
        method: Literal["email", "facebook"] = "email",
    ) -> list[dict[str, Any]]:
        """Get most shared articles

        Args:
            days (Literal[1, 7, 30], optional): Period of the most shared
            articles. Defaults to 1.
            method (Literal["email, "facebook"], optional): Choose the source
            of shared articles. Defaults to "email".

        Returns:
            list[dict[str, Any]]: Most shared articles
        """
        most_shared_check_days(days)
        most_shared_check_method(method)

        # Set URL of data that needs to be loaded
        url = most_shared_get_url(BASE_MOST_POPULAR, method, days)

        # Load the data
        result: list[dict[str, Any]] = self.__load_data(url)  # type:ignore

        # Parse the date_strings into datetime.datetime
        parsed_result = self.__parse_dates(
            self.__parse_dates(result, "date-only", ["published_date"]),
            "date-time",
            ["updated"],
        )

        return parsed_result

    def book_reviews(
        self,
        author: Optional[str] = None,
        isbn: Optional[Union[str, int]] = None,
        title: Optional[str] = None,
    ) -> list[dict[str, Any]]:
        """Load book reviews

        Args:
            author (Optional[str], optional): Name of author. Defaults to None.
            isbn (Optional[Union[str, int]], optional): ISBN of book. Defaults to None.
            title (Optional[str], optional): Title of book. Defaults to None.

        Returns:
            list[dict[str, Any]]: Reviews of books
        """
        # Set request options params
        options = book_reviews_extract_options(author, isbn, title)

        # Check book review input
        book_reviews_check_input(author, isbn, title)

        # Set URL, load and return data
        result: list[dict[str, Any]] = self.__load_data(
            url=BASE_BOOK_REVIEWS, options=options
        )  # type:ignore

        parsed_result = self.__parse_dates(result, "date-only", ["publication_dt"])
        return parsed_result

    def best_sellers_lists(self) -> list[dict[str, Any]]:
        """Get all the best sellers lists (not the contents of these lists,
        but just all the lists).

        Returns:
            list[dict[str, Any]]: Bestsellers lists
        """
        # Set URL, load and return data
        result = cast(
            list[dict[str, Any]],
            self.__load_data(url=BASE_BEST_SELLERS_LISTS),
        )

        parsed_result = self.__parse_dates(
            result,
            "date-only",
            ["oldest_published_date", "newest_published_date"],
        )
        return parsed_result

    def best_sellers_list(
        self,
        date: Optional[DateType] = None,
        name: str = "combined-print-and-e-book-fiction",
    ) -> list[dict[str, Any]]:
        """Load all books on a best sellers lists

        Args:
            date (Union[datetime.date, datetime.datetime, None], optional):
            The list closest to this date. If left empty loads most recent.
            Defaults to None.
            name (str, optional): Name of the list. Defaults to
            "combined-print-and-e-book-fiction".

        Raises:
            ValueError: List does not exist

        Returns:
            list[dict[str, Any]]: Books that are on the best sellers list
        """
        _date = best_sellers_parse_date(date)

        # Set URL and include data
        url = f"{BASE_BEST_SELLERS_LIST}{_date}/{name}.json"

        # Set location in JSON of results, load and return data
        try:
            result = cast(
                list[dict[str, Any]],
                self.__load_data(url, location=["results", "books"]),
            )
        except RuntimeError:
            raise ValueError("Best sellers list name is invalid")

        return result

    def __load_movie_reviews(
        self, max_results: int, params: dict[str, Any]
    ) -> list[dict[str, Any]]:
        # Set results list
        results: list[dict[str, Any]] = []

        requests_needed = math.ceil(max_results / RESULTS_MOVIE)
        for i in range(requests_needed):
            # Set offset for second request
            offset = i * RESULTS_MOVIE
            params["offset"] = str(offset)

            # Load the data from the API and raise if there's an Error
            res = cast(
                dict[str, Any],
                self.__load_data(
                    url=BASE_MOVIE_REVIEWS,
                    options=params,
                    location=[],
                ),
            )

            results += res.get("results")  # type:ignore

            # Quit loading more data if no more data is available
            if not res.get("has_more"):
                break

        return results

    def movie_reviews(
        self,
        keyword: Optional[str] = None,
        options: Optional[MovieReviewsOptions] = None,
        dates: Optional[dict[Literal["begin", "end"], DateType]] = None,
    ) -> list[dict[str, Any]]:
        """Load movie reviews

        Args:
            keyword (Optional[str], optional): Keyword to find the movie.
            Defaults to None.
            options (Optional[dict[str, Any]], optional): Options object
            where certain requirements can be set. Check for more
            https://github.com/michadenheijer/pynytimes. Defaults to None.
            dates (Optional[MovieReviewsDateType],
            optional):
            Dates between the review was written or movie was first shown.
            Defaults to None.

        Returns:
            list[dict[str, Any]]: Movie reviews
        """
        warnings.warn(
            "This function is deprecated and will be removed in the next version.",
            DeprecationWarning,
        )

        # Set options and dates if not defined
        _options = cast(dict[str, Any], options or {})
        dates = dates or {}

        # Check input types and values
        movie_reviews_check_input(keyword, _options, dates)
        params = movie_reviews_parse_dates(dates)
        movie_reviews_parse_params(params, keyword, _options)

        max_results = _options.get("max_results", RESULTS_MOVIE)
        results = self.__load_movie_reviews(max_results, params)

        # Parse and return the results
        # FIXME this part really seems unclear
        parsed_results = self.__parse_dates(
            self.__parse_dates(
                results, "date-only", ["publication_date", "opening_date"]
            ),
            "date-time",
            ["date_updated"],
        )

        return parsed_results

    def article_metadata(self, url: str) -> list[dict[str, Any]]:
        """Load metadata of an article by url

        Args:
            url (str): URL of an New York Times article

        Returns:
            list[dict[str, Any]]: List of article metadata
        """
        warnings.warn(
            "This function is deprecated and will be removed in the next version.",
            DeprecationWarning,
        )
        options = article_metadata_set_url(url)

        # Load, parse and return the data
        result = cast(
            list[dict[str, Any]],
            self.__load_data(url=BASE_META_DATA, options=options),
        )

        article_metadata_check_valid(result)

        # FIXME this looks like it should be a constant
        date_locations = [
            "updated_date",
            "created_date",
            "published_date",
            "first_published_date",
        ]
        parsed_result = self.__parse_dates(result, "rfc3339", date_locations)
        return parsed_result

    def section_list(self) -> list[dict[str, Any]]:
        """Load all list of all sections

        Returns:
            list[dict[str, Any]]: List of sections
        """
        # Set URL, load and return the data
        return cast(
            list[dict[str, Any]],
            self.__load_data(url=BASE_SECTION_LIST),
        )

    def latest_articles(
        self,
        source: Literal["all", "nyt", "inyt"] = "all",
        section: str = "all",
    ) -> list[dict[str, Any]]:
        """Load latest articles

        Args:
            source (Literal["all", "nyt", "inyt"], optional): Select sources to get all
            articles from. Defaults to "all".
            section (str, optional): Section to get all latest articles from.
            Defaults to "all".

        Raises:
            ValueError: Section is not a valid option

        Returns:
            list[dict[str, Any]]: List of metadata of latest articles
        """
        latest_articles_check_types(source, section)

        # Set URL, load and return data
        url = f"{BASE_LATEST_ARTICLES}{source}/{section}.json"
        try:
            result = cast(list[dict[str, Any]], self.__load_data(url))
        except RuntimeError:
            raise ValueError("Section is not a valid option")

        # FIXME looks like this should be a constant
        date_locations = [
            "updated_date",
            "created_date",
            "published_date",
            "first_published_date",
        ]
        parsed_result = self.__parse_dates(result, "rfc3339", date_locations)
        return parsed_result

    def tag_query(
        self,
        query: str,
        filter_option: Optional[dict[str, Any]] = None,
        filter_options: Optional[str] = None,
        max_results: Optional[int] = None,
    ) -> list[str]:
        """Load Times Tags

        Args:
            query (str): Search query to find a tag
            filter_option (Optional[dict[str, Any]], optional): Filter the tags.
            Defaults to None.
            filter_options (Optional[str], optional): Filter options. Defaults
            to None.
            max_results (Optional[int], optional): Maximum number of results.
            None means no limit. Defaults to None.

        Returns:
            list[str]: List of tags
        """
        # Raise error for TypeError
        tag_query_check_types(query, max_results)

        _filter_options = tag_query_get_filter_options(filter_options) or filter_option

        # Add options to request params
        options = {"query": query, "filter": _filter_options}

        # Define amount of results wanted
        if max_results is not None:
            options["max"] = str(max_results)

        # Set URL, load and return data
        # FIXME what is this, why is this?
        return self.__load_data(url=BASE_TAGS, options=options, location=[])[
            1
        ]  # type:ignore

    def archive_metadata(self, date: DateType) -> list[dict[str, Any]]:
        """Load all article metadata from the last month

        Args:
            date (Union[datetime.datetime, datetime.date]): The month of
            which you want to load all article metadata from

        Raises:
            TypeError: Date is not a datetime or date object

        Returns:
            list[dict[str, Any]]: List of article metadata
        """
        # Raise Error if date is not defined
        if not isinstance(date, (datetime.datetime, datetime.date)):
            raise TypeError("Date has to be datetime or date")

        # Set URL, load and return data
        url = f"{BASE_ARCHIVE_METADATA}{date.year}/{date.month}.json"

        # FIXME why not return immidiatly? what it is doing is also unclear
        parsed_result = self.__parse_dates(
            self.__load_data(  # type:ignore
                url, location=["response", "docs"]
            ),
            "rfc3339",
            ["pub_date"],
        )
        return parsed_result

    # FIXME should this not be in a helper function?
    def __article_search_load_data(
        self,
        results: int,
        options: dict[str, Any],
    ) -> list[dict[str, Any]]:
        result = []
        for i in range(math.ceil(results / RESULTS_SEARCH)):
            # Set page
            options["page"] = str(i)

            location = ["response"]
            # Load data and raise error if there's and error status
            res: dict[str, Any] = self.__load_data(  # type:ignore
                url=BASE_ARTICLE_SEARCH, options=options, location=location
            )

            # Parse results and append them to results list
            result += res.get("docs")  # type:ignore

            # Stop loading if all responses are already loaded
            if res.get("meta", {}).get("hits", 0) <= i * RESULTS_SEARCH:
                break

        return result

    # FIXME this appears to try to do to much
    def article_search(
        self,
        query: Optional[str] = None,
        dates: Optional[dict[Literal["begin", "end"], DateType]] = None,
        options: Optional[ArticleSearchOptions] = None,
        results: int = 10,
    ) -> list[dict[str, Any]]:
        """Search New York Times articles

        Args:
            query (Optional[str], optional): Search query. Defaults to None.
            dates (Optional[dict[Literal["begin", "end"], DateType]],
            optional): Dictionary with "begin" and "end" of search range.
            Defaults to None.
            options (Optional[ArticleSearchOptions], optional): Options for the
            search results.
            Defaults to None.
            results (int, optional): Load at most this many articles. Defaults to 10.

        Returns:
            list[dict[str, Any]]: Article metadata
        """
        # Set if None
        dates = dates or {}
        _options = cast(dict[str, Any], options or {})

        # Check if input is valid
        article_search_check_input(query, dates, _options, results)

        # Limit results loading to 2010
        results = min(results, 2010)

        # Resolve filter options into fq
        _options = article_search_parse_options(_options)

        # Parse dates into options
        # FIXME I really don't get this error
        begin_date, end_date = article_search_parse_dates(dates)
        _options["begin_date"] = begin_date
        _options["end_date"] = end_date

        # Set query if defined
        if query is not None:
            _options["q"] = query

        # Set result list and add request as much data as needed
        result = self.__article_search_load_data(results, _options)

        # Parse and return results
        parsed_result = self.__parse_dates(result, "rfc3339", ["pub_date"])
        return parsed_result

    # Allow the option to close the session
    def close(self) -> None:
        """Close session"""
        # Close session only if it exists
        if hasattr(self, "session"):
            self.session.close()

    # Close session before delete
    def __del__(self) -> None:
        """Close session on deletion"""
        if getattr(self, "_local_session", False):
            self.close()

    def __exit__(self, *args) -> None:
        """Close session on exit"""
        if getattr(self, "_local_session", False):
            self.close()
