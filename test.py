import datetime

from pynytimes import nytAPI


nyt = nytAPI("DgKALEQLVaCWyoZlfiJNAPPrsmY3MHaA")
print(nyt.best_sellers_list(date=datetime.datetime(2019, 10, 20)))