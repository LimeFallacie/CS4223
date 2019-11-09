

class Core:
    def __init__(self, input):
        self.inputFile = input
        self.stall = False
        self.completed = False
        self.stallCount = 0  # for counting stall cycles for /other instructions/
        self.instCount = 0
        self.instrlist = []

    # reads data from file, returns list of instructions
    def dataread(self):
        data = open(self.inputFile, 'r')
        instrlist = data.readlines()
        self.instrlist = instrlist
        for i in range(4):
            print(self.instrlist.pop(0))
