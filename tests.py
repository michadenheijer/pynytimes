# type: ignore
import datetime
import unittest

import os
import time
import random
from pynytimes import NYTAPI

API_KEY = os.environ["NewYorkTimesAPIKey"]


class TestNewYorkTimes(unittest.TestCase):
    def setUp(self):
        self.nyt = NYTAPI(API_KEY, parse_dates=True)

    def tearDown(self):
        self.nyt.close()

    def test_empty_api_key(self):
        with self.assertRaises(TypeError):
            NYTAPI()

    def test_top_stories(self):
        top_stories = self.nyt.top_stories()
        self.assertIsInstance(top_stories, list)
        self.assertGreater(len(top_stories), 0)

        for top_story in top_stories:
            self.assertIsInstance(top_story, dict)
            self.assertIsInstance(top_story["created_date"], datetime.datetime)
            self.assertIsInstance(top_story["published_date"], datetime.datetime)

    def test_top_stories_section(self):
        section = "world"
        top_stories_section = self.nyt.top_stories(section=section)
        self.assertIsInstance(top_stories_section, list)
        self.assertGreater(len(top_stories_section), 0)

        for top_story in top_stories_section:
            self.assertIsInstance(top_story, dict)

    def test_top_stories_wrong_section(self):
        with self.assertRaises(ValueError):
            self.nyt.top_stories("abcdfsda")

        with self.assertRaises(TypeError):
            self.nyt.top_stories(section=123)

    def test_most_viewed(self):
        most_viewed = self.nyt.most_viewed()
        self.assertIsInstance(most_viewed, list)
        self.assertGreater(len(most_viewed), 0)

        for most in most_viewed:
            self.assertIsInstance(most, dict)
            self.assertIsInstance(most["media"], list)

    def test_most_viewed_invalid_days(self):
        with self.assertRaises(ValueError):
            self.nyt.most_viewed(2)

        with self.assertRaises(TypeError):
            self.nyt.most_viewed(days="1")

    def test_most_shared(self):
        most_shared = self.nyt.most_shared()
        self.assertIsInstance(most_shared, list)
        self.assertGreater(len(most_shared), 0)

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
        author = "Barack Obama"
        book_reviews = self.nyt.book_reviews(author=author)
        self.assertIsInstance(book_reviews, list)
        self.assertGreater(len(book_reviews), 0)

        for book_review in book_reviews:
            self.assertIsInstance(book_review, dict)
            self.assertEqual(book_review["book_author"], author)

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
        self.assertGreater(len(best_sellers_lists), 0)

    def test_best_seller_list(self):
        best_seller_list = self.nyt.best_sellers_list(
            date=datetime.datetime(2019, 1, 1), name="hardcover-fiction"
        )
        self.assertIsInstance(best_seller_list, list)
        self.assertEqual(best_seller_list[0]["primary_isbn13"], "9780385544153")

    def test_best_seller_list_invalid(self):
        with self.assertRaises(ValueError):
            self.nyt.best_sellers_list(name="not a name")

        with self.assertRaises(TypeError):
            self.nyt.best_sellers_list(date="123")

    # FIXME This function is not working, thus this test is removed for now
    # def test_movie_reviews(self):
    #     movie_reviews = self.nyt.movie_reviews()
    #     self.assertIsInstance(movie_reviews, list)
    #     self.assertGreater(len(movie_reviews), 0)

    #     for movie_review in movie_reviews:
    #         self.assertIsInstance(movie_review, dict)

    # FIXME This function is not working, thus this test is removed for now
    # def test_movie_reviews_invalid(self):
    #     with self.assertRaises(TypeError):
    #         self.nyt.movie_reviews(keyword=123)

    # FIXME This function is not working, thus this test is removed for now
    # def test_article_metadata(self):
    #     article_metadata = self.nyt.article_metadata(
    #         "https://www.nytimes.com/live/2021/02/10/us/impeachment-trial/prosecutors-begin-arguments-against-trump-saying-he-became-the-inciter-in-chief-of-a-dangerous-insurrection"
    #     )
    #     self.assertIsInstance(article_metadata, list)

    #     for article in article_metadata:
    #         self.assertIsInstance(article, dict)

    #     title = "Prosecutors argue that Trump ‘became the inciter in chief’ and retell riot with explicit video."
    #     creation_datetime = datetime.datetime(
    #         2021,
    #         2,
    #         10,
    #         11,
    #         4,
    #         8,
    #         tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=68400)),
    #     )
    #     self.assertEqual(article_metadata[0]["title"], title)
    #     self.assertEqual(
    #         article_metadata[0]["created_date"],
    #         creation_datetime,
    #     )

    # FIXME This function is not working, thus this test is removed for now
    # def test_article_metadata_invalid(self):
    #     with self.assertRaises(TypeError):
    #         self.nyt.article_metadata()

    #     with self.assertRaises(TypeError):
    #         self.nyt.article_metadata(123)

    #     with self.assertRaises(ValueError):
    #         self.nyt.article_metadata("text")

    def test_archive_metadata(self):
        archive_metadata = self.nyt.archive_metadata(date=datetime.date.today())
        self.assertIsInstance(archive_metadata, list)
        self.assertGreater(len(archive_metadata), 0)

        for metadata in archive_metadata:
            self.assertIsInstance(metadata, dict)
            self.assertGreaterEqual(
                metadata["pub_date"],
                datetime.datetime.now(tz=datetime.timezone.utc).replace(
                    day=1, hour=0, minute=0, second=0, microsecond=0
                ),
            )

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

    def test_article_search_headline(self):
        headline_query = "Biden"
        search = self.nyt.article_search(options={"headline": [headline_query]})
        self.assertIsInstance(search, list)
        for article in search:
            self.assertIsInstance(article, dict)
            self.assertIn(headline_query, str(article["headline"]))

    def test_article_search_invalid(self):
        with self.assertRaises(TypeError):
            self.nyt.article_search(123)

        with self.assertRaises(TypeError):
            self.nyt.article_search("query", datetime.date.today())

    def test_section_list(self):
        section_list = self.nyt.section_list()
        self.assertIsInstance(section_list, list)
        self.assertGreater(len(section_list), 0)

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

    # FIXME This needs test needs to be written for a different function as this function is not working
    # def test_parse_dates_disabled(self):
    #     local_nyt = NYTAPI(API_KEY)
    #     data = local_nyt.article_metadata(
    #         "https://www.nytimes.com/live/2021/02/10/us/impeachment-trial/prosecutors-begin-arguments-against-trump-saying-he-became-the-inciter-in-chief-of-a-dangerous-insurrection"
    #     )

    #     self.assertEqual(data[0]["created_date"], "2021-02-10T11:04:08-05:00")


if __name__ == "__main__":
    if os.environ.get("FULL_TESTS", False):
        random_sleep_seconds = random.choice([0, 20, 40, 60, 80, 100])
        print(f"Run full tests, Sleep {random_sleep_seconds} seconds.")
        time.sleep(random_sleep_seconds)
    unittest.main()
