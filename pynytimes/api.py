"""The wrapper is here"""
import datetime
import math

import requests

BASE_TOP_STORIES = "https://api.nytimes.com/svc/topstories/v2/"
BASE_MOST_POPULAR = "https://api.nytimes.com/svc/mostpopular/v2/"
BASE_BOOKS = "https://api.nytimes.com/svc/books/v3/"
BASE_MOVIE_REVIEWS = "https://api.nytimes.com/svc/movies/v2/reviews/search.json"
BASE_META_DATA = "https://api.nytimes.com/svc/news/v3/content.json"
BASE_TAGS = "https://api.nytimes.com/svc/suggest/v1/timestags.json"
BASE_BOOK_REVIEWS = BASE_BOOKS + "reviews.json"
BASE_BEST_SELLERS_LISTS = BASE_BOOKS + "lists/names.json"
BASE_BEST_SELLERS_LIST = BASE_BOOKS + "lists/"




class GetResults:
    """In this class the data gets fetched from the New York Times Servers"""
    @staticmethod
    def top_stories(key, section):
        """Get the Top Stories"""
        api_key = {"api-key": key}
        url = BASE_TOP_STORIES + section + ".json"
        res = requests.get(url, params=api_key)
        res.raise_for_status()
        results = res.json().get("results")
        return results

    @staticmethod
    def most_viewed(key, days):
        """Get the most viewed articles"""
        api_key = {"api-key": key}
        url = BASE_MOST_POPULAR + "viewed/" + str(days) + ".json"
        res = requests.get(url, params=api_key)
        res.raise_for_status()
        results = res.json().get("results")
        return results

    @staticmethod
    def most_shared(key, days, method):
        """Get the most shared articles"""
        api_key = {"api-key": key}
        if method is None:
            url = BASE_MOST_POPULAR + "shared/" + str(days) + ".json"
        else:
            url = BASE_MOST_POPULAR + "shared/" + str(days) + "/" + method + ".json"
        res = requests.get(url, params=api_key)
        res.raise_for_status()
        results = res.json().get("results")
        return results

    @staticmethod
    def book_reviews(key, author, isbn, title):
        """Get book reviews"""
        params = {
            "api-key": key
        }
        if author is not None:
            params["author"] = author

        elif isbn is not None:
            params["isbn"] = str(isbn)

        elif title is not None:
            params["title"] = title

        url = BASE_BOOK_REVIEWS
        res = requests.get(url, params=params)
        results = res.json().get("results")
        return results

    @staticmethod
    def best_sellers_lists(key):
        """Get the best sellers lists"""
        api_key = {"api-key": key}
        url = BASE_BEST_SELLERS_LISTS
        res = requests.get(url, params=api_key)
        res.raise_for_status()
        results = res.json().get("results")
        return results

    @staticmethod
    def best_sellers_list(key, date, name):
        """Get a best sellers list"""
        api_key = {"api-key": key}
        url = BASE_BEST_SELLERS_LIST + date + "/" + name + ".json"
        res = requests.get(url, params=api_key)
        res.raise_for_status()
        results = res.json().get("results").get("books")
        return results

    @staticmethod
    def movie_reviews(key, keyword, options, max_results):
        """Get movie reviews"""
        params = {"api-key": key}

        if keyword is not None:
            params["query"] = keyword

        params["critics-pick"] = options.get("critics")
        params["reviewer"] = options.get("reviewer")
        params["order"] = options.get("order")
        params["opening-date"] = options.get("opening")
        params["publication-date"] = options.get("publication")

        url = BASE_MOVIE_REVIEWS

        results = []

        for i in range(math.ceil(max_results/20)):
            offset = i*20
            params["offset"] = str(offset)
            res = requests.get(url, params=params)
            res.raise_for_status()
            res_parsed = res.json()
            results += res_parsed.get("results")

            if res_parsed.get("has_more") is False:
                break

        return results

    @staticmethod
    def article_metadata(key, url):
        """Get the article metadata"""
        params = {
            "api-key": key,
            "url": url
        }
        url = BASE_META_DATA

        res = requests.get(url, params=params)
        res.raise_for_status()
        result = res.json().get("results")

        return result

    @staticmethod
    def tags(key, query, filter_options, max_results):
        """Get TimesTags"""
        params = {
            "api-key": key,
            "query": query,
            "filter": filter_options
        }
        if max_results is not None:
            params["max"] = str(max_results)

        url = BASE_TAGS

        res = requests.get(url, params=params)
        res.raise_for_status()
        result = res.json()

        return result


class NYTAPI:
    """This class interacts with the Python code, it primarily blocks wrong user input"""
    def __init__(self, key=None):
        self.key = key
        if self.key is None:
            raise Exception("No API key")

    def top_stories(self, section=None):
        """Load the top stories"""
        if section is None:
            section = "home"

        return GetResults.top_stories(self.key, section)

    def most_viewed(self, days=None):
        """Load most viewed articles"""
        days_options = [1, 7, 30]
        if days is None:
            days = 1

        if days not in days_options:
            raise Exception("You can only select 1, 7 or 30 days")

        return GetResults.most_viewed(self.key, days)

    def most_shared(self, days=None, method=None):
        """Load most shared articles"""
        method_options = ["email", "facebook", "twitter"]
        days_options = [1, 7, 30]

        if days is None:
            days = 1

        if method not in method_options:
            raise Exception("Shared option does not exist")

        if days not in days_options:
            raise Exception("You can only select 1, 7 or 30 days")

        return GetResults.most_shared(self.key, days, method)

    def book_reviews(self, author=None, isbn=None, title=None):
        """Load book reviews"""
        if author and isbn and title is None:
            raise Exception("Not all fields in reviews can be empty")

        if int(isbn is not None) + int(title is not None) + int(author is not None) != 1:
            raise Exception("You can only define one of the following: ISBN, author or title.")

        return GetResults.book_reviews(self.key, author, isbn, title)

    def best_sellers_lists(self):
        """Load all the best seller lists"""
        return GetResults.best_sellers_lists(self.key)

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

        return GetResults.best_sellers_list(self.key, _date, name)

    def movie_reviews(
            self,
            keyword=None,
            options=None):
        """Load movie reviews"""
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

        if options.get("critics") is True:
            _critics_pick = "Y"

        settings = {
            "critics": _critics_pick,
            "reviewer": options.get("reviewer"),
            "order": options.get("order"),
            "opening": _opening_dates,
            "publication": _publication_dates
        }

        return GetResults.movie_reviews(self.key,
                                        keyword,
                                        settings,
                                        options.get("max_results", 20))

    def article_metadata(self, url):
        """Load the metadata from an article"""
        return GetResults.article_metadata(self.key, url)

    def tags(self, query, filter_option=None, filter_options=None, max_results=None):
        """Load TimesTags"""
        _filter_options = ""
        if filter_options is not None:
            for filter_opt in filter_options:
                if _filter_options is not None:
                    _filter_options += ","

                _filter_options += filter_opt

        elif filter_option is not None:
            _filter_options = filter_option

        return GetResults.tags(self.key, query, _filter_options, max_results)
