import sys

#constants
WORD_SIZE = 4;
BLOCK_SIZE = 32;
CACHE_SIZE = 4096;
ASSOCIATIVITY = 2;


def main():
    if not (len(sys.argv)==3 or len(sys.argv) == 6):
        sys.exit("wrong number of arguments: " + str(len(sys.argv)))

    protocol = sys.argv[1]
    input = sys.argv[2]
    cacheSize = CACHE_SIZE
    assoc = ASSOCIATIVITY
    blockSize = BLOCK_SIZE

    if len(sys.argv) == 3:
        cacheSize = sys.argv[3]
        assoc = sys.argv[4]
        blockSize = sys.argv[5]


    print("============CONFIG============\n")
    # script arguments parsed here [coherence “protocol” “input_file” “cache_size” “associativity” “block_size”]
    print("protocol = %s" % protocol)
    print("input file = %s" % input)
    print("cache size = %s" % cacheSize)
    print("assoc = %s" % assoc)
    print("block size = %s" % blockSize)

    cores = []
    for i in range(1, 5):
        # TODO cores initialisation
        cores.append("core")

    print("\n\n\n")
    print("============Results============\n")
    # script arguments parsed here [coherence “protocol” “input_file” “cache_size” “associativity” “block_size”]
    print("overall cycle count = %s" % "PLACEHOLDER")
    for i in range(1, 5):
        print("======== core %s ========" % i)
        print("cycle count for core %d = %s" % (i, "PLACEHOLDER"))
        print("load/store instruction count for core %d = %s" % (i, "PLACEHOLDER"))
        print("idle cycle count for core %d = %s" % (i, "PLACEHOLDER"))
        print("data cache miss rate for core %d = %s%%" % (i, "PLACEHOLDER"))
    print("========================")
    print("bus data traffic in bytes = %s" % "PLACEHOLDER")
    print("number of invalidation or update in bus = %s" % "PLACEHOLDER")
    print("private data versus shared data access distribution = %s%%" % "PLACEHOLDER")



if __name__ == '__main__':
    main()
