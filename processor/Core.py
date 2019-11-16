from cache import MESI, Dragon


class Core:
    def __init__(self, protocol, input, cache_size, associativity, block_size):
        self.inputFile = input
        self.stall = False
        self.completed = False
        self.stallCount = 0  # for counting stall cycles for instr execution
        self.instCount = 0  # counts total num instr already read
        self.instrlist = []  # list of instr lines
        self.dataread()
        if protocol.upper() == 'MESI':
            self.controller = MESI(cache_size, associativity, block_size, self)
        elif protocol.lower() == 'dragon':
            self.controller = Dragon(cache_size, associativity, block_size, self)

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
            print(command[2:])
            bin_command = bin(int(command[2:].strip(), 16))[2:].zfill(32)  # converts the hex string to binary
            print(bin_command)  # bin_command is currently a string
            if command[:1] == '0':  # load
                self.get_controller().prRd(int(bin_command, 2))
            elif command[:1] == '1':  # store
                self.get_controller().prWr(int(bin_command, 2))
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

    def check_done(self):
        if self.instrlist[0].strip() == "":
            return True
        else:
            return False
