import datetime
import unittest

import os
from pynytimes import NYTAPI

API_KEY = os.environ["NewYorkTimesAPIKey"]


class TestNewYorkTimes(unittest.TestCase):
    def setUp(self):
        self.nyt = NYTAPI(API_KEY, parse_dates=True)

    def tearDown(self):
        self.nyt.close()

    def test_empty_api_key(self):
        with self.assertRaises(ValueError):
            NYTAPI()

    def test_top_stories(self):
        top_stories = self.nyt.top_stories()
        self.assertIsInstance(top_stories, list)
        self.assertIsInstance(top_stories[0], dict)

    def test_top_stories_section(self):
        top_stories_section = self.nyt.top_stories(section="world")
        self.assertIsInstance(top_stories_section, list)
        self.assertIsInstance(top_stories_section[0], dict)

    def test_top_stories_wrong_section(self):
        with self.assertRaises(ValueError):
            self.nyt.top_stories("abcdfsda")

        with self.assertRaises(TypeError):
            self.nyt.top_stories(section=123)

    def test_most_viewed(self):
        most_viewed = self.nyt.most_viewed()
        self.assertIsInstance(most_viewed, list)
        for most in most_viewed:
            self.assertIsInstance(most, dict)
            self.assertIsInstance(most["media"], list)

    def test_most_viewed_invalid_days(self):
        with self.assertRaises(ValueError):
            self.nyt.most_viewed(days=2)

        with self.assertRaises(TypeError):
            self.nyt.most_viewed(days="1")

    def test_most_shared(self):
        most_shared = self.nyt.most_shared()
        self.assertIsInstance(most_shared, list)
        for most in most_shared:
            self.assertIsInstance(most, dict)
            self.assertIsInstance(most["published_date"], datetime.date)
            self.assertIsInstance(most["updated"], datetime.datetime)
            self.assertIsInstance(most["media"], list)

    def test_most_shared_invalid(self):
        with self.assertRaises(ValueError):
            self.nyt.most_shared(method="twitter")

        with self.assertRaises(ValueError):
            self.nyt.most_shared(days=2)

        with self.assertRaises(TypeError):
            self.nyt.most_shared(days="2")

    def test_book_reviews(self):
        book_reviews = self.nyt.book_reviews(author="Barack Obama")
        self.assertIsInstance(book_reviews, list)
        for book_review in book_reviews:
            self.assertIsInstance(book_review, dict)

    def test_book_reviews_invalid(self):
        with self.assertRaises(ValueError):
            self.nyt.book_reviews()

        with self.assertRaises(ValueError):
            self.nyt.book_reviews(isbn=213789, author="author")

        with self.assertRaises(ValueError):
            self.nyt.book_reviews(isbn=213789)

    def test_best_sellers_lists(self):
        best_sellers_lists = self.nyt.best_sellers_lists()
        self.assertIsInstance(best_sellers_lists, list)

    def test_best_seller_list(self):
        best_seller_list = self.nyt.best_sellers_list(
            date=datetime.datetime(2019, 1, 1), name="hardcover-fiction"
        )
        self.assertIsInstance(best_seller_list, list)

    def test_best_seller_list_invalid(self):
        with self.assertRaises(ValueError):
            self.nyt.best_sellers_list(name="not a name")

        with self.assertRaises(TypeError):
            self.nyt.best_sellers_list(date="123")

    def test_movie_reviews(self):
        movie_reviews = self.nyt.movie_reviews()
        self.assertIsInstance(movie_reviews, list)

        for movie_review in movie_reviews:
            self.assertIsInstance(movie_review, dict)

    def test_movie_reviews_invalid(self):
        with self.assertRaises(TypeError):
            self.nyt.movie_reviews(keyword=123)

    def test_article_metadata(self):
        article_metadata = self.nyt.article_metadata(
            "https://www.nytimes.com/live/2021/02/10/us/impeachment-trial/prosecutors-begin-arguments-against-trump-saying-he-became-the-inciter-in-chief-of-a-dangerous-insurrection"
        )
        self.assertIsInstance(article_metadata, list)
        for article in article_metadata:
            self.assertIsInstance(article, dict)

    def test_article_metadata_invalid(self):
        with self.assertRaises(TypeError):
            self.nyt.article_metadata()

        with self.assertRaises(TypeError):
            self.nyt.article_metadata(123)

        with self.assertRaises(ValueError):
            self.nyt.article_metadata("text")

    def test_archive_metadata(self):
        archive_metadata = self.nyt.archive_metadata(date=datetime.date.today())
        self.assertIsInstance(archive_metadata, list)
        for metadata in archive_metadata:
            self.assertIsInstance(metadata, dict)

    def test_archive_metadata_invalid(self):
        with self.assertRaises(TypeError):
            self.nyt.archive_metadata("string")

        with self.assertRaises(TypeError):
            self.nyt.archive_metadata(123)

    def test_article_search(self):
        search = self.nyt.article_search("Joe Biden", results=80)
        self.assertIsInstance(search, list)
        self.assertEqual(80, len(search))
        for article in search:
            self.assertIsInstance(article, dict)

    def test_article_search_invalid(self):
        with self.assertRaises(TypeError):
            self.nyt.article_search(123)

        with self.assertRaises(TypeError):
            self.nyt.article_search("query", datetime.date.today())

    def test_section_list(self):
        section_list = self.nyt.section_list()
        self.assertIsInstance(section_list, list)
        for section in section_list:
            self.assertIsInstance(section, dict)

    def test_latest_articles(self):
        latest_articles = self.nyt.latest_articles()
        self.assertIsInstance(latest_articles, list)

        for article in latest_articles:
            self.assertIsInstance(article, dict)

    def test_latest_articles_invalid(self):
        with self.assertRaises(TypeError):
            self.nyt.latest_articles(source=123)

    def test_tag_query(self):
        tags = self.nyt.tag_query("Obama", max_results=2)
        self.assertIsInstance(tags, list)
        self.assertIs(2, len(tags))

    def test_tag_query_invalid(self):
        with self.assertRaises(TypeError):
            self.nyt.tag_query(123)

        with self.assertRaises(TypeError):
            self.nyt.tag_query("Obama", max_results="2")


if __name__ == "__main__":
    unittest.main()