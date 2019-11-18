from cache import Constants

class Bus:
    def __init__(self, controllers, block_size, block_update):
        #pass in snoopers
        self.controllers = controllers
        for each in controllers:
            each.connect_bus(self)
        #init transaction queue
        self.transaction_list = []
        self.block_size = block_size
        self.block_update = block_update
        self.shared = False
        self.wait_counter = 0
        self.source_core = -1
        
       

    def add_transaction(self, transaction):
        self.transaction_list.append(transaction)
        
    def nextTick(self):
        if (self.wait_counter > 1):
            self.wait_counter -= 1
            return
        
        elif(self.source_core >= 0):
            self.controllers[self.source_core].unstall(self.shared)
            self.shared = False
            self.source_core = -1
            return
        
        if len(self.transaction_list):
            next_transaction = self.transaction_list.pop(0)
            self.process(next_transaction)
        
    def process(self, transaction):
        #init list of potential caches that are sharing cache block
        cache_sharing = []
        self.source_core = transaction.get_source()
        for i in range(len(self.controllers)):
            if (i != self.source_core) and (self.controllers[i].snoop(transaction)):
                self.shared = True
                cache_sharing.append(i)
        
        can_provide = False
        
        if (transaction.get_transaction == Constants.TransactionTypes.BusRd):
            for i in cache_sharing:
                if (self.controllers[i].can_provide()):
                    can_provide = True
                    break
            if (can_provide):
                self.wait_counter = self.block_update
            else:
                wait_counter = Constant.BusConstants.MISS
            
        elif (transaction.get_transaction == Constants.TransactionTypes.BusRdX):
            for i in cache_sharing:
                if (self.controllers[i].can_provide()):
                    can_provide = True
                    break
            if (can_provide):
                self.wait_counter = self.block_update
            else:
                self.wait_counter = Constant.BusConstants.MISS
                
        elif (transaction.get_transaction == Constants.TransactionTypes.BusUpd):
            self.wait_counter = Constant.BusConstants.UPDATE          
                
                
class Transaction:
    def __init__(self, transaction_type, source, address):
        self.transaction_type = transaction_type
        self.source = source
        self.address = address
        
    def get_transaction(self):
        return self.transaction_type
    
    def get_source(self):
        return self.source.get_identifier()

    def get_address(self):
        return self.address


