import math
from collections import deque
from cache import Constants


class CacheBlock:
    def __init__(self, tag, state, dirty):
        self.tag = tag
        self.state = state
        self.dirty = dirty

    def get_tag(self):
        return self.tag

    def set_tag(self, new_tag):
        self.tag = new_tag

    def get_state(self):
        return self.state

    def set_state(self, new_state):
        self.state = new_state

    def is_dirty(self):
        return self.dirty

    def set_dirty(self):
        self.dirty = True


class CacheSet:
    def __init__(self, associativity):
        self.associativity = associativity
        self.cacheBlocks = []
        # queue with index of LRU cacheblock on leftmost
        self.LRUindex = deque()
        # sets
        for i in range(0, associativity):
            self.LRUindex.append(i)
            self.cacheBlocks.append(CacheBlock(0, Constants.States.INVALID, False))

    def contains(self, tag):
        for block in self.cacheBlocks:
            if block.get_tag() == tag:
                return True
        return False

    def add(self, cache_block):
        index = self.LRUindex.popleft()
        block = self.cacheBlocks.pop(index)
        self.cacheBlocks.insert(index, cache_block)
        self.LRUindex.append(index)
        if block.is_dirty():
            return True
        else:
            return False

            # prerequisite : data is found in cache set
    def get_state(self, tag):
        for block in self.cacheBlocks:
            if block.get_tag() == tag:
                return block.get_state()
        return Constants.States.INVALID

    # prerequisite : data is found in cache set
    def update_state(self, tag, state, dirty = False):
        for block in self.cacheBlocks:
            if block.get_tag() == tag:
                block.set_state(state)  # update state
                if dirty:
                    block.set_dirty()

    def update_dirty(self, tag):
        for block in self.cacheBlocks:
            if block.get_tag() == tag:
                block.set_dirty()  # update dirty


    def get_LRU_index(self, cache_block):
        cache_index = self.cacheBlocks.index(cache_block)
        return self.LRUindex.index(cache_index)

    # prerequisite : data is found in cache set
    def access(self, tag):
        for block in self.cacheBlocks:
            if block.get_tag() == tag:
                index = self.get_LRU_index(block)
                self.LRUindex.append(list(self.LRUindex).pop(index))

    # prerequisite : data is found in cache set
    def access_and_write(self, tag):
        for block in self.cacheBlocks:
            if block.get_tag() == tag:
                index = self.get_LRU_index(block)
                self.LRUindex.append(list(self.LRUindex).pop(index))
                block.set_dirty()


class Cache:
    def __init__(self, size, associativity, block_size):
        set_size = int(size / (block_size * associativity))
        self.indexBits = int(math.log(set_size, 2))
        self.offsetBits = int(math.log(block_size, 2))
        self.tagBits = 32 - self.indexBits - self.offsetBits
        self.cacheSets = []
        # indexes
        for i in range(0, set_size):
            self.cacheSets.append(CacheSet(associativity))
        # print(len(self.cacheSets))
        self.missCount = 0
        self.accessCount = 0

    # obtain the index value
    # prerequisite: address is 32 bits
    def get_index(self, address):
        # print("getting index from "+ address[self.tagBits : 32 - self.offsetBits])
        addressStr = str(address)
        return int(addressStr[self.tagBits : 32 - self.offsetBits], 2)

    # obtain the tag value
    # prerequisite: address is 32 bits
    def get_tag(self, address):
        addressStr = str(address)
        return int(addressStr[ : 32 - self.indexBits - self.offsetBits])

    def add_to_cache(self, address, state, dirty=False):
        cache_set = self.cacheSets[self.get_index(address)]
        return cache_set.add(CacheBlock(self.get_tag(address), state, dirty))

    def contains(self, address):
        # print(address)
        # print(self.get_index(address))
        cache_set = self.cacheSets[self.get_index(address)]
        return cache_set.contains(self.get_tag(address))

    def get_state(self, address):
        cache_set = self.cacheSets[self.get_index(address)]
        return cache_set.get_state(self.get_tag(address))

    def update_state(self, address, state, dirty = False):
        cache_set = self.cacheSets[self.get_index(address)]
        cache_set.update_state(self.get_tag(address), state, dirty)

    def update_dirty(self, address):
        cache_set = self.cacheSets[self.get_index(address)]
        cache_set.update_dirty(self.get_tag(address))

    def access(self, address):
        cache_set = self.cacheSets[self.get_index(address)]
        cache_set.access(self.get_tag(address))

    def access_and_write(self, address):
        cache_set = self.cacheSets[self.get_index(address)]
        cache_set.access_and_write(self.get_tag(address))

    # debug
    def printCache(self):
        i = 0
        for set in self.cacheSets:
            print("### index %d ###" % i)
            j = 0
            for block in set.cacheBlocks:
                print("  set%3d: %32d, %s" % (j, block.tag, block.state))
                j += 1
            i += 1
