from cache import CacheController, Constants
from bus import Transaction


class Dragon(CacheController):

    def busUpd(self, address):
        self.core.stall()
        self.bus.add_transaction(Transaction(Constants.TransactionTypes.BusUpd, self.core, address))

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
            elif (self.cache.get_state(address) == Constants.States.SHARED_CLEAN or
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
                self.cache.access(address)
            # data is in E state
            elif self.cache.get_state(address) == Constants.States.EXCLUSIVE:
                self.privAccess += 1
                self.hit += 1
                self.cache.update_state(address, Constants.States.MODIFIED)
            # data is in SC or SM state
            elif (self.cache.get_state(address) == Constants.States.SHARED_CLEAN or
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
                    self.cache.update_state(transaction.get_address(), Constants.States.SHARED_CLEAN)
                    # data is to be copied over to target cache
                    return True
            # data is in SC state
            elif self.cache.update_state(transaction.get_address()) == Constants.States.SHARED_CLEAN:
                # transaction is BusRd
                if transaction.get_transaction() == Constants.TransactionTypes.BusRd:
                    self.cache.update_state(transaction.get_address(), Constants.States.SHARED_CLEAN)
                    # data is to be copied over to target cache
                    return True
                # transaction is BusUpd
                if transaction.get_transaction() == Constants.TransactionTypes.BusUpd:
                    self.cache.update_state(transaction.get_address(), Constants.States.SHARED_CLEAN)
                    # data does not need to be copied to target cache
                    return False
            # data is in SM state
            elif self.cache.get_state(transaction.get_address()) == Constants.States.SHARED_MODIFIED:
                # transaction is BusRd
                if transaction.get_transaction() == Constants.TransactionTypes.BusRd:
                    self.cache.update_state(transaction.get_address(), Constants.States.SHARED_MODIFIED)
                    # data is to be copied over to target cache
                    return True
                # transaction is BusUpd
                elif transaction.get_transaction() == Constants.TransactionTypes.BusUpd:
                    # immediate request to writeback
                    self.bus.writeback(transaction.get_address())
                    self.cache.update_state(transaction.get_address(), Constants.States.SHARED_CLEAN)
                    # data does not need to be copied to target cache
                    return False
            # data is in M state
            elif self.cache.update_state(transaction.get_address()) == Constants.States.MODIFIED:
                # transaction is BusRd
                if transaction.get_transaction() == Constants.TransactionTypes.BusRd:
                    self.cache.update_state(transaction.get_address(), Constants.States.SHARED_MODIFIED)
                    # data is to be copied over to target cache
                    return True

