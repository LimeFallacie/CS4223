from cache import CacheController, Constants


class MESI(CacheController):
    
    def unstall(self, shared):
        if (self.unstall_address == -1): #state after eviction
            self.unstall()
            self.stalled = False
            return
        
        unstall_state = ""
        writeback = False
        dirty = False

        if self.unstall_action == "PrRd":
            unstall_state = Constants.States.SHARED if shared else Constants.States.EXCLUSIVE 
            
        else:
            unstall_state = Constants.States.MODIFIED
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
        self.unstall_address = address
        self.unstall_action = "PrRd"
        # data is present in cache
        if self.cache.contains(address):
            # data is in M or E state
            if (self.cache.get_state(address) == Constants.States.MODIFIED or
                    self.cache.get_state(address) == Constants.States.EXCLUSIVE):
                self.hit += 1
                self.privAccess += 1
                self.cache.access(address)
            # data is in S state
            elif self.cache.get_state(address) == Constants.States.SHARED:
                self.hit += 1
                self.pubAccess += 1
                self.cache.access(address)
            # data is in I state
            elif self.cache.get_state(address) == Constants.States.INVALID:
                self.miss += 1
                self.busRd(address)
        # data is not present in cache
        else:
            self.miss += 1
            self.busRd(address)

    def prWr(self, address):
        self.unstall_address = address
        self.unstall_action = "PrWr"
    # data is present in cache
        if self.cache.contains(address):
            # data is in M or E state
            if (self.cache.get_state(address) == Constants.States.MODIFIED or
                    self.cache.get_state(address) == Constants.States.EXCLUSIVE):
                self.privAccess += 1
                self.hit += 1
                self.cache.update_state(address, Constants.States.MODIFIED, True)
            # data is in S state
            elif self.cache.get_state(address) == Constants.States.SHARED:
                self.pubAccess += 1
                self.hit += 1
                self.busRdX(address)
            # data is in I state
            elif self.cache.get_state(address) == Constants.States.INVALID:
                self.miss += 1
                self.busRdX(address)
        # data is not present in cache
        else:
            self.miss += 1
            self.busRdX(address)

    def snoop(self, transaction):
        # data is not present in cache
        if not self.cache.contains(transaction.get_address()):
            #print("core", self.core.identifier, " does not have ", transaction.address, " for core", transaction.source.identifier)
            return False

        else:
            #print("core", self.core.identifier, " has ", transaction.address, " for core", transaction.source.identifier, " state is ", self.cache.get_state(transaction.get_address()))

            # data is in M state
            if self.cache.get_state(transaction.get_address()) == Constants.States.MODIFIED:
                # immediate request to writeback
                #self.bus.writeback(transaction.get_address())
                # transaction is BusRd
                if transaction.get_transaction() == Constants.TransactionTypes.BusRd:
                    self.cache.update_state(transaction.get_address(), Constants.States.SHARED)
                # transaction is BusRdX
                elif transaction.get_transaction() == Constants.TransactionTypes.BusRdX:
                    self.cache.update_state(transaction.get_address(), Constants.States.INVALID)
                # data is to be copied over to target cache
                self.can_provide_flag = True
                return True
            # data is in E state
            elif self.cache.get_state(transaction.get_address()) == Constants.States.EXCLUSIVE:
                # transaction is BusRd
                if transaction.get_transaction() == Constants.TransactionTypes.BusRd:
                    self.cache.update_state(transaction.get_address(), Constants.States.SHARED)
                # transaction is BusRdX
                elif transaction.get_transaction() == Constants.TransactionTypes.BusRdX:
                    self.cache.update_state(transaction.get_address(), Constants.States.INVALID)
                # data is to be copied over to target cache
                self.can_provide_flag = True
                return True
            # data is in S state
            elif self.cache.get_state(transaction.get_address()) == Constants.States.SHARED:
                # transaction is BusRd
                if transaction.get_transaction() == Constants.TransactionTypes.BusRd:
                    self.can_provide_flag = True
                    return True
                # transaction is BusRdX
                elif transaction.get_transaction() == Constants.TransactionTypes.BusRdX:
                    self.cache.update_state(transaction.get_address(), Constants.States.INVALID)
                    # data does not need to be copied to target cache
                    return False
            # data is in I state
            elif self.cache.get_state(transaction.get_address()) == Constants.States.INVALID:
                return False
