import sys, os
from processor import Core
from bus import Bus
import time

#constants
DEFAULT_WORD_SIZE = 4;
DEFAULT_BLOCK_SIZE = 32;
DEFAULT_CACHE_SIZE = 4096;
DEFAULT_ASSOCIATIVITY = 2;


def main():
    t0 = time.time()
    if not (len(sys.argv) == 3 or len(sys.argv) == 6):
        sys.exit("wrong number of arguments: " + str(len(sys.argv)))

    protocol = sys.argv[1]
    input = sys.argv[2]
    cacheSize = DEFAULT_CACHE_SIZE
    assoc = DEFAULT_ASSOCIATIVITY
    blockSize = DEFAULT_BLOCK_SIZE

    if len(sys.argv) == 6:
        cacheSize = int(sys.argv[3])
        assoc = int(sys.argv[4])
        blockSize = int(sys.argv[5])

    print("============CONFIG============\n")
    # script arguments parsed here [coherence “protocol” “input_file” “cache_size” “associativity” “block_size”]
    print("protocol = %s" % protocol)
    print("input file = %s" % input)
    if input == 'fluid':
        input = input + 'animate'
    print("cache size = %s" % cacheSize)
    print("assoc = %s" % assoc)
    print("block size = %s" % blockSize)

    cwd = os.getcwd()
    benchmark = '\\benchmarks\\' + input + '\\' + input + '_'
    benchmark = cwd + benchmark
    # print(benchmark)

    cores = []
    controllers = []  # for passing into Bus constructor later
    for i in range(4):
        percore = benchmark + str(i) + '.data'  # appends index and file type .data
        cores.append(Core(protocol, percore.replace('\\', '/'), cacheSize, assoc, blockSize, i))  # replace all \\ with / because python sys paths are weird
        controllers.append(cores[i].get_controller())
    bus = Bus(controllers, blockSize, blockSize/DEFAULT_WORD_SIZE)

    completed = False
    check = [False, False, False, False]  # all 4 cores not completed yet
    progress = 0
    total_cycles = 0
    while not completed:
        total_cycles += 1
        for i in range(4):
            if not cores[i].check_done():
                cores[i].nextTick()
            elif not check[i]:  # if core[i] done, check[i] = True
                check[i] = True
                progress += 1  # once progress = 4 break
            else:
                pass
        bus.nextTick()
        if progress == 4:
            completed = True

    print("\n\n\n")

    for i in range(4):
        total_cycles = max(total_cycles, cores[i].exec_cycles)

    print("============RESULTS============\n")
    # script arguments parsed here [coherence “protocol” “input_file” “cache_size” “associativity” “block_size”]
    print("overall cycle count = %s" % total_cycles)
    for i in range(1, 5):
        print("======== core %s ========" % i)
        print("execution cycles for core %d = %s" % (i, cores[i-1].exec_cycles))
        print("cycle count for core %d = %s" % (i, cores[i-1].get_computeCycles()))
        print("load/store instruction count for core %d = %s" % (i, cores[i-1].get_LDSTR()))
        print("idle cycle count for core %d = %s" % (i, cores[i-1].idle_cycles))
        print("data cache miss rate for core %d = %s%%" % (i, controllers[i-1].get_miss_rate()))
        print("private data access distribution for core %d = %s%%" % (i, controllers[i-1].get_priv_rate()))
        print("public data access distribution for core %d = %s%%" % (i, controllers[i - 1].get_pub_rate()))
    print("========================")
    print("bus data traffic in bytes = %s" % str(bus.get_data_traffic()))
    print("number of invalidation or update in bus = %s" % str(bus.get_invalidations()))
    t1 = time.time()
    print("time taken = %d seconds" % (t1 - t0))


if __name__ == '__main__':
    main()
