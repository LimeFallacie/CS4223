class States:
    MODIFIED = "M"
    EXCLUSIVE = "E"
    SHARED = "S"
    INVALID = "I"
    SHARED_MODIFIED = "SM"


class TransactionTypes:
    BusRd = "BUSRD"
    BusRdX = "BUSRDX"
    BusUpd = "BUSUPD"
    
class BusConstants:
    MISS = 100
    EVICTION = 99
    UPDATE = 1
    WORDSIZE = 4
