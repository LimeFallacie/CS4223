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

    if not len(sys.argv == 3):
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


if __name__ == '__main__':
    main()
