import requests

base_top_stories = "https://api.nytimes.com/svc/topstories/v2/"
base_most_popular = "https://api.nytimes.com/svc/mostpopular/v2/"
class API(object):
    def __init__(self, key=None):
        self.key = key
        if self.key is None:
            raise Exception("No API key")

    def _get_top_stories(self, section):
        api_key = { "api-key": self.key }
        url = base_top_stories + section + ".json"
        res = requests.get(url, params=api_key)
        res.raise_for_status()
        results =  res.json()["results"]
        return results

    def _get_most_viewed(self, days):
        api_key = { "api-key": self.key }
        url = base_most_popular + "viewed/" + str(days) + ".json"
        res = requests.get(url, params=api_key)
        res.raise_for_status()
        results = res.json()["results"]
        return results

    def _get_most_shared(self, days, method):
        api_key = { "api-key": self.key }
        url = base_most_popular + "shared/" + str(days) + "/" + method + ".json"
        res = requests.get(url, params=api_key)
        res.raise_for_status()
        results = res.json()["results"]
        return results

    def top_stories(self, section=None):
        if section is None:
            section = "home"

        return API._get_top_stories(self, section)

    def most_viewed(self, days=None):
        days_options = [1, 7, 30]
        if days is None:
            days = 1

        if days not in days_options:
            raise Exception("You can only select 1, 7 or 30 days")

        return API._get_most_viewed(self, days)
        
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

        return API._get_most_shared(self, days, method)