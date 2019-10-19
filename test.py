import datetime

from pynytimes import NYTAPI


nyt = NYTAPI("DgKALEQLVaCWyoZlfiJNAPPrsmY3MHaA")
print(nyt.tags("pentagon", max_results=3, filter_options=["Des", "Per"]))