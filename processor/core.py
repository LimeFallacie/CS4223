from cache import MESI,Dragon

class Core:
    def __init__(self, protocol, input):
        self.inputFile = input
        self.stall = False
        self.completed = False
        self.stallCount = 0  # for counting stall cycles for instr execution
        self.instCount = 0  # counts total num instr already read
        self.instrlist = []  # list of instr lines
        self.dataread()
        if protocol.upper() == 'MESI':
            self.controller = MESI()
        elif protocol.lower() == 'dragon':
            self.controller = Dragon()

    # reads data from file, returns list of instructions
    def dataread(self):
        data = open(self.inputFile, 'r')
        instrlist = data.readlines()
        self.instrlist = instrlist

    def stall(self):
        print("Core running " + self.inputFile + "has been stalled\n")
        self.stall = True

    def nextTick(self):
        if not self.stall and (self.stallCount == 0):
            self.instCount += 1
            command = self.instrlist.pop(0).strip()  # pops the front of the list and removes lead/trailing whitespace
            if command[:1] == '0':  # load
                pass  # TODO: fill in PrRd case
            elif command[:1] == '1':  # store
                pass  # TODO: fill in PrWr case
            elif command[:1] == '2':  # other
                # set self.stallCount value for stall timer
                self.stallCount = int(command[2:].strip(), 16)  # removes label value, strips whitespaces, converts hex to int
                print("Core running " + self.inputFile + " will be stalled for " + self.stallCount + " cycles")
            else:
                return False

        elif not self.stall and (self.stallCount > 0):
            self.stallCount -= 1
            if self.stallCount == 0:
                self.stall = False

    def get_controller(self):
        return self.controller
