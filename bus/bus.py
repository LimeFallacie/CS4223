

class Transaction:
    def __init__(self, tran, source, address):
        self.tran = tran
        self.source = source
        self.address = address
        
    def get_transaction(self):
        return self.tran
    
    def get_source(self):
        return self.source

    def get_address(self):
        return self.address


class Bus:
    def __init__(self, tranList):
        self.transList = transList
        #init snoopers here
        
    def add_transaction(self, tran):
        self.transList.append(tran)
        
    