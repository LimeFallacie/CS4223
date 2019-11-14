from abc import ABC, abstractmethod
from cache import CacheController


class MESI(CacheController):
    def __init__(self):
        print(issubclass(MESI, CacheController))


if __name__=='__main__':
    MESI()
