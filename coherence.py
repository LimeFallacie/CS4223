import sys

#constants
WORD_SIZE = 4;
BLOCK_SIZE = 16;
CACHE_SIZE = 4096;
ASSOCIATIVITY = 1;

print("============CONFIG============\n")
# script arguments parsed here [coherence “protocol” “input_file” “cache_size” “associativity” “block_size”]
print("protocol = %s" % sys.argv[1])
print("input file = %s" % sys.argv[2])
print("cache size = %s" % sys.argv[3])
print("assoc = %s" % sys.argv[4])
print("block size = %s" % sys.argv[5])



