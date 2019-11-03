

# read the input file here?
class Processor:
    def __init__(self, input):
        self.inputFile = input
        self.stall = False
        self.completed = False
        self.stallCount = 0 # for counting stall cycles for /other instructions/
        self.instCount = 0

