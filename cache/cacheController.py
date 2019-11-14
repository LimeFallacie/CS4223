from processor import core
import cache

class CacheController:
    def __init__(self, size, associativity, block_size):
        self.cache = Cache(size, associativity, block_size)
        self.hit = 0
        self.miss = 0
        
        
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