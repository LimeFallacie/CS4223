from abc import ABC, abstractmethod
from cache import CacheController


class MESI(CacheController):
    def __init__(self):
        print('MESI constructor has been called')
        print(self)


if __name__=='__main__':
    MESI()
