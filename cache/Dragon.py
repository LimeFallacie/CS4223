from cache import Cache, CacheController, Constants
from bus import Transaction


class Dragon(CacheController):
    
    def unstall(self, shared):
        if (self.unstall_address == -1): #state after eviction
            self.unstall()
            self.stalled = False
            return
        unstall_state = ""
        writeback = False
        dirty = False
        
        if (self.unstall_action == Constants.UnstallAction.PrRd):
            unstall_state = Constants.States.SHARED if shared else Constants.States.EXCLUSIVE
            
        elif (self.unstall_action == Constants.UnstallAction.BusUpd):
            unstall_state = Constants.States.SHARED_MODIFIED if shared else Constants.States.MODIFIED
            dirty = True

        else:
            unstall_state = Constants.States.SHARED_MODIFIED
            dirty = True

        if self.cache.contains(self.unstall_address):
            self.cache.update_state(self.unstall_address, unstall_state, dirty)
        else:
            writeback = self.cache.add_to_cache(self.unstall_address, unstall_state, dirty)
        #else:
            #eviction necessary here
            
        self.unstall_address = 0
        self.unstall_action = ""
        
        self.core.unstall()
        self.stalled = False
        
        return writeback

    def prRd(self, address):
        # data is present in cache
        if self.cache.contains(address):
            # data is in M or E state
            if (self.cache.get_state(address) == Constants.States.MODIFIED or
                    self.cache.get_state(address) == Constants.States.EXCLUSIVE):
                self.hit += 1
                self.privAccess += 1
                self.cache.access(address)
            # data is in SC or SM state
            elif (self.cache.get_state(address) == Constants.States.SHARED or
                  self.cache.get_state(address) == Constants.States.SHARED_MODIFIED):
                self.hit += 1
                self.pubAccess += 1
                self.cache.access(address)
        # data is not present in cache
        else:
            self.miss += 1
            self.busRd(address)

    def prWr(self, address):
        # data is present in cache
        if self.cache.contains(address):
            # data is in M state
            if self.cache.get_state(address) == Constants.States.MODIFIED:
                self.privAccess += 1
                self.hit += 1
                self.cache.access_and_write(address)
            # data is in E state
            elif self.cache.get_state(address) == Constants.States.EXCLUSIVE:
                self.privAccess += 1
                self.hit += 1
                self.cache.update_state(address, Constants.States.MODIFIED, True)
            # data is in SC or SM state
            elif (self.cache.get_state(address) == Constants.States.SHARED or
                  self.cache.get_state(address) == Constants.States.SHARED_MODIFIED):
                self.pubAccess += 1
                self.hit += 1
                self.busUpd(address)
        # data is not present in cache
        else:
            self.miss += 1
            self.busRd(address)

    def snoop(self, transaction):
        # data is not present in cache
        if not self.cache.contains(transaction.get_address()):
            return False

        else:
            # data is in E state
            if self.cache.get_state(transaction.get_address()) == Constants.States.EXCLUSIVE:
                # transaction is BusRd
                if transaction.get_transaction() == Constants.TransactionTypes.BusRd:
                    self.cache.update_state(transaction.get_address(), Constants.States.SHARED)
                    # data is to be copied over to target cache
                    self.can_provide_flag = True
                    return True
            # data is in SC state
            elif self.cache.get_state(transaction.get_address()) == Constants.States.SHARED:
                # transaction is BusUpd
                if transaction.get_transaction() == Constants.TransactionTypes.BusUpd:
                    self.cache.update_state(transaction.get_address(), Constants.States.SHARED)
                    # data does not need to be copied to target cache
                    return False
            # data is in SM state
            elif self.cache.get_state(transaction.get_address()) == Constants.States.SHARED_MODIFIED:
                # transaction is BusRd
                if transaction.get_transaction() == Constants.TransactionTypes.BusRd:
                    self.cache.update_state(transaction.get_address(), Constants.States.SHARED_MODIFIED)
                    # data is to be copied over to target cache
                    self.can_provide_flag = True
                    return True
                # transaction is BusUpd
                elif transaction.get_transaction() == Constants.TransactionTypes.BusUpd:
                    # immediate request to writeback
                    self.cache.update_state(transaction.get_address(), Constants.States.SHARED)
                    # data does not need to be copied to target cache
                    return False
            # data is in M state
            elif self.cache.get_state(transaction.get_address()) == Constants.States.MODIFIED:
                # transaction is BusRd
                if transaction.get_transaction() == Constants.TransactionTypes.BusRd:
                    self.cache.update_state(transaction.get_address(), Constants.States.SHARED_MODIFIED)
                    # data is to be copied over to target cache
                    self.can_provide_flag = True
                    return True

