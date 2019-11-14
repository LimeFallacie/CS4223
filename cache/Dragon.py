from abc import ABC, abstractmethod
from cache import CacheController


class Dragon(CacheController):
    def __init__(self):
        print('Dragon constructor has been called')
        print(self)


if __name__=='__main__':
    Dragon()
