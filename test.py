import pynytimes

nyt = pynytimes.API("DgKALEQLVaCWyoZlfiJNAPPrsmY3MHaA")
print(nyt.most_shared(days=30))