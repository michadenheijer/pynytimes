import datetime

from pynytimes import nytAPI


nyt = nytAPI("DgKALEQLVaCWyoZlfiJNAPPrsmY3MHaA")
print(nyt.movie_reviews(max_results=80))