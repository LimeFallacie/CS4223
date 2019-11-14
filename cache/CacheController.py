from cache import Cache, Constants
from bus import Transaction
from abc import ABC, abstractmethod


class CacheController(ABC):

    def __init__(self, size, associativity, block_size, core):
        self.cache = Cache(size, associativity, block_size)
        self.hit = 0
        self.miss = 0
        self.privAccess = 0
        self.pubAccess = 0
        self.core = core

    def stall(self):
        self.core.stall()

    def connect_bus(self, bus):
        self.bus = bus

    def get_miss_rate(self):
        return 100 * self.miss / (self.hit+self.miss)

    def get_hit(self):
        return self.hit

    def get_miss(self):
        return self.miss

    def busRd(self, address):
        self.core.stall()
        self.bus.add_transaction(Transaction(Constants.TransactionTypes.BusRd, self.core, address))

    def busRdX(self, address):
        self.core.stall()
        self.bus.add_transaction(Transaction(Constants.TransactionTypes.BusRdX, self.core, address))

    @abstractmethod
    def prRd(self, address):
        pass

    @abstractmethod
    def prWr(self, address):
        pass

    # returns true if data is to be copied, false if data is not to be copied
    @abstractmethod
    def snoop(self, transaction):
        pass
