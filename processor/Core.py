from cache import MESI, Dragon, MOESI
from collections import deque


class Core:
    def __init__(self, protocol, input, cache_size, associativity, block_size, identifier):
        self.inputFile = input
        self.stalled = False
        self.completed = False
        self.stallCount = 0  # for counting stall cycles for instr execution
        self.instCount = 0  # counts total num instr already read
        self.instrlist = deque()  # list of instr lines
        self.dataread()
        self.identifier = identifier
        self.compute_cycles = 0
        self.ldr_and_str = 0
        self.exec_cycles = 0
        self.idle_cycles = 0
        if protocol.upper() == 'MESI':
            self.controller = MESI(cache_size, associativity, block_size, self)
        elif protocol.lower() == 'dragon':
            self.controller = Dragon(cache_size, associativity, block_size, self)
        elif protocol.upper() == 'MOESI':
            self.controller = MOESI(cache_size, associativity, block_size, self)
            
    def get_identifier(self):
        return self.identifier

    # reads data from file, returns list of instructions
    def dataread(self):
        data = open(self.inputFile, 'r')
        instrlist = data.readlines()
        for line in instrlist:
            self.instrlist.append(line)

    def stall(self):
        # print("Core running " + self.inputFile + " has been stalled\n")
        self.stalled = True
        
    def unstall(self):
        # print("Core running " + self.inputFile + " has been unstalled\n")
        self.stalled = False

    def nextTick(self):
        self.exec_cycles += 1
        if not self.stalled and (self.stallCount == 0):
            self.instCount += 1
            command = self.instrlist.popleft().strip()  # pops the front of the list and removes lead/trailing whitespace
            bin_command = bin(int(command[2:].strip(), 16))[2:].zfill(32)  # converts the hex string to binary

            # print("id = " + str(self.identifier) + "\tprogress = " + str(self.instCount))
            # print(command)
            # print(bin_command)
            if command[:1] == '0':  # load
                self.ldr_and_str += 1
                self.get_controller().prRd(bin_command)
            elif command[:1] == '1':  # store
                self.ldr_and_str += 1
                self.get_controller().prWr(bin_command)
            elif command[:1] == '2':  # other
                # set self.stallCount value for stall timer
                self.stall()
                self.stallCount = int(command[2:].strip(), 16)
                self.compute_cycles += self.stallCount
                # print("Core running " + self.inputFile + " will be stalled for " + str(self.stallCount) + " cycles")
            else:
                return False

        elif self.stalled and (self.stallCount > 0):  # executing label 2
            self.stallCount -= 1
            if self.stallCount == 0:
                self.unstall()
        else:
            self.idle_cycles += 1

    def get_controller(self):
        return self.controller

    def check_done(self):
        if (not self.instrlist) and (not self.stalled):
            return True
        else:
            return False

    def get_instCount(self):
        return self.instCount

    def get_computeCycles(self):
        return self.compute_cycles

    def get_LDSTR(self):
        return self.ldr_and_str
