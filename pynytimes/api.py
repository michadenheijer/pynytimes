import datetime

import requests

base_top_stories = "https://api.nytimes.com/svc/topstories/v2/"
base_most_popular = "https://api.nytimes.com/svc/mostpopular/v2/"
base_books = "https://api.nytimes.com/svc/books/v3/"
base_book_reviews = base_books + "reviews.json"
base_best_sellers_lists = base_books + "lists/names.json"
base_best_sellers_list = base_books + "lists/"



class _get_results:
    def top_stories(key, section):
        api_key = { "api-key": key }
        url = base_top_stories + section + ".json"
        res = requests.get(url, params=api_key)
        res.raise_for_status()
        results =  res.json().get("results")
        return results

    def most_viewed(key, days):
        api_key = { "api-key": key }
        url = base_most_popular + "viewed/" + str(days) + ".json"
        res = requests.get(url, params=api_key)
        res.raise_for_status()
        results = res.json().get("results")
        return results

    def most_shared(key, days, method):
        api_key = { "api-key": key }
        url = base_most_popular + "shared/" + str(days) + "/" + method + ".json"
        res = requests.get(url, params=api_key)
        res.raise_for_status()
        results = res.json().get("results")
        return results

    def book_reviews(key, author, isbn, title):
        params = {
            "api-key": key
        }
        if author is not None:
            params["author"] = author

        elif isbn is not None:
            params["isbn"] = str(isbn)

        elif title is not None:
            params["title"] = title

        url = base_book_reviews 
        res = requests.get(url, params=params)
        results = res.json().get("results")
        return results

    def best_sellers_lists(key):
        api_key = { "api-key": key }
        url = base_best_sellers_lists
        res = requests.get(url, params=api_key)
        results = res.json().get("results")
        return results

    def best_sellers_list(key, date, name):
        api_key = { "api-key": key }
        url = base_best_sellers_list + date + "/" + name + ".json"
        res = requests.get(url, params=api_key)
        results = res.json().get("results").get("books")
        return results

class nytAPI(object):
    def __init__(self, key=None):
        self.key = key
        if self.key is None:
            raise Exception("No API key")

    def top_stories(self, section=None):
        if section is None:
            section = "home"

        return _get_results.top_stories(self.key, section)

    def most_viewed(self, days=None):
        days_options = [1, 7, 30]
        if days is None:
            days = 1

        if days not in days_options:
            raise Exception("You can only select 1, 7 or 30 days")

        return _get_results.most_viewed(self.key, days)
        
    def most_shared(self, days=None, method=None):
        method_options = ["email", "facebook", "twitter"]
        days_options = [1, 7, 30]
        
        if method is None:
            method = "email"

        if days is None:
            days = 1

        if method not in method_options:
            raise Exception("Shared option does not exist")

        if days not in days_options:
            raise Exception("You can only select 1, 7 or 30 days")

        return _get_results.most_shared(self.key, days, method)

    def book_reviews(self, author=None, isbn=None, title=None):
        if author and isbn and title is None:
            raise Exception("Not all fields in reviews can be empty")

        if int(isbn is not None) + int(title is not None) + int(author is not None) is not 1:
            raise Exception("You can only define one of the following: ISBN, author or title.")

        return _get_results.book_reviews(self.key, author, isbn, title)

    def best_sellers_lists(self):
        return _get_results.best_sellers_lists(self.key)

    def best_sellers_list(self, date=None, name=None):
        if date is None:
            _date = "current"
        
        elif not isinstance(date, datetime.datetime):
            raise Exception("Date has to be a datetime object")

        else:
            _date = date.strftime("%Y-%m-%d")

        if name is None:
            name = "combined-print-and-e-book-fiction"
        
        return _get_results.best_sellers_list(self.key, _date, name)
