from cache import CacheController, Constants


class MESI(CacheController):

    def prRd(self, address):
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
        # data is present in cache
        if self.cache.contains(address):
            # data is in M or E state
            if (self.cache.get_state(address) == Constants.States.MODIFIED or
                    self.cache.get_state(address) == Constants.States.EXCLUSIVE):
                self.privAccess += 1
                self.hit += 1
                self.cache.update_state(address, Constants.States.MODIFIED)
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
            return False

        else:
            # data is in M state
            if self.cache.get_state(transaction.get_address()) == Constants.States.MODIFIED:
                # immediate request to writeback
                self.bus.writeback(transaction.get_address())
                # transaction is BusRd
                if transaction.get_transaction() == Constants.TransactionTypes.BusRd:
                    self.cache.update_state(transaction.get_address(), Constants.States.SHARED)
                # transaction is BusRdX
                elif transaction.get_transaction() == Constants.TransactionTypes.BusRdX:
                    self.cache.update_state(transaction.get_address(), Constants.States.INVALID)
                # data is to be copied over to target cache
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
                return True
            # data is in S state
            elif self.cache.update_state(transaction.get_address()) == Constants.States.SHARED:
                # transaction is BusRdX
                if transaction.get_transaction() == Constants.TransactionTypes.BusRdX:
                    self.cache.update_state(transaction.get_address(), Constants.States.INVALID)
                # data does not need to be copied to target cache
                return False
            # data is in I state
            elif self.cache.update_state(transaction.get_address()) == Constants.States.INVALID:
                return False
