from prtpy import BinsKeepingContents
from prtpy.partitioning.rnp import rnp
from prtpy.partitioning.snp import snp
from time import perf_counter

if __name__ == '__main__':

    start = perf_counter()

    items = [4,5,6,7,8]

    for i in range(0,10):

        print(rnp(BinsKeepingContents(3), items=items).sums)
        items.append(i)

    end = perf_counter()
    print(end - start)