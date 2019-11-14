class States:
    MODIFIED = "M"
    EXCLUSIVE = "E"
    SHARED = "S"
    INVALID = "I"
    SHARED_CLEAN = "SC"
    SHARED_MODIFIED = "SM"


class TransactionTypes:
    BusRd = "BUSRD"
    BusRdX = "BUSRDX"
    BusUpd = "BUSUPD"
