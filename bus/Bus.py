

class Bus:
    def __init__(self, controllers):
        self.controllers = controllers
        for each in controllers:
            each.connect_bus(self)
        self.transaction_list = []
        # init snoopers here

    def add_transaction(self, transaction):
        self.transaction_list.append(transaction)


class Transaction:
    def __init__(self, transaction_type, source, address):
        self.transaction_type = transaction_type
        self.source = source
        self.address = address
        
    def get_transaction(self):
        return self.transaction_type
    
    def get_source(self):
        return self.source

    def get_address(self):
        return self.address


