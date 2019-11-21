from cache import CacheController, Constants


class MOESI(CacheController):

    def unstall(self, shared):
        unstall_state = ""
        writeback = False
        dirty = False

        if self.unstall_action == Constants.UnstallAction.PrRd:
            unstall_state = Constants.States.SHARED if shared else Constants.States.EXCLUSIVE
        elif self.unstall_action == Constants.UnstallAction.PrWr:
            unstall_state = Constants.States.MODIFIED
            dirty = True

        if self.cache.contains(self.unstall_address):
            self.cache.update_state(self.unstall_address, unstall_state, dirty)
        else:
            writeback = self.cache.add_to_cache(self.unstall_address, unstall_state, dirty)

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
            # data in M or E state
            if (self.cache.get_state(address) == Constants.States.MODIFIED or
                    self.cache.get_state(address) == Constants.States.EXCLUSIVE):
                self.hit += 1
                self.privAccess += 1
                self.cache.access(address)
            # data in S or O state
            elif (self.cache.get_state(address) == Constants.States.SHARED or
                    self.cache.get_state(address) == Constants.States.SHARED_MODIFIED):
                self.hit += 1
                self.pubAccess += 1
                self.cache.access(address)
            # data is in I state
            elif self.cache.get_state(address) == Constants.States.INVALID:
                self.miss += 1
                self.busRd(address)
        # data not present in cache
        else:
            self.miss += 1
            self.busRd(address)

    def prWr(self, address):
        self.unstall_address = address
        self.unstall_action = "PrWr"
        # data is present in cache
        if self.cache.contains(address):
            # data in M or E state
            if (self.cache.get_state(address) == Constants.States.MODIFIED or
                    self.cache.get_state(address) == Constants.States.EXCLUSIVE):
                self.privAccess += 1
                self.hit += 1
                self.cache.update_state(address, Constants.States.MODIFIED, True)
            # data is in S or O state
            elif (self.cache.get_state(address) == Constants.States.SHARED or
                      self.cache.get_state(address) == Constants.States.SHARED_MODIFIED):
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
        address = transaction.get_address()
        type = transaction.get_transaction()

        # data is not present in cache
        if not self.cache.contains(address):
            return False

        else:
            # data is in M state
            if self.cache.get_state(address) == Constants.States.MODIFIED:
                # transaction is BusRd
                if type == Constants.TransactionTypes.BusRd:
                    self.cache.update_state(address, Constants.States.SHARED_MODIFIED)
                # transaction is BusRdX
                elif type == Constants.TransactionTypes.BusRdX:
                    self.cache.update_state(address, Constants.States.INVALID)
                # data can be obtained
                self.can_provide_flag = True
                return True
            # E state
            elif self.cache.get_state(address) == Constants.States.EXCLUSIVE:
                # BusRd
                if type == Constants.TransactionTypes.BusRd:
                    self.cache.update_state(address, Constants.States.SHARED)
                # BusRdX
                elif type == Constants.TransactionTypes.BusRdX:
                    self.cache.update_state(address, Constants.States.INVALID)
                # data can be obtained
                self.can_provide_flag = True
                return True
            # O and S state
            elif (self.cache.get_state(address) == Constants.States.SHARED_MODIFIED or
                      self.cache.get_state(address) == Constants.States.SHARED):
                # BusRd
                if type == Constants.TransactionTypes.BusRd:
                    pass
                # BusRdX
                elif type == Constants.TransactionTypes.BusRdX:
                    self.cache.update_state(address, Constants.States.INVALID)
                # data can be obtained
                self.can_provide_flag = True
                return True
            # I state
            elif self.cache.get_state(address) == Constants.States.INVALID:
                return False