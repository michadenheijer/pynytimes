import datetime

from pynytimes import NYTAPI


nyt = NYTAPI("DgKALEQLVaCWyoZlfiJNAPPrsmY3MHaA")
print(nyt.archive_metadata(datetime.datetime(2019, 1, 1)))