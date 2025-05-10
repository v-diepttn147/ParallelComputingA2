import time
import threading
import random
from coarse_grained_set import CoarseGrainedSet
from fine_grained_set import FineGrainedSet

def benchmark(set_class, num_threads=4, operations_per_thread=5000):
    s = set_class()

    def worker():
        for _ in range(operations_per_thread):
            op = random.choice(['add', 'remove', 'contains'])
            val = random.randint(1, 1000)
            if op == 'add':
                s.add(val)
            elif op == 'remove':
                s.remove(val)
            else:
                s.contains(val)

    threads = [threading.Thread(target=worker) for _ in range(num_threads)]
    start = time.perf_counter()
    for t in threads: t.start()
    for t in threads: t.join()
    end = time.perf_counter()
    return end - start

if __name__ == "__main__":
    for cls in [CoarseGrainedSet, FineGrainedSet]:
        for n in [1, 2, 4, 8]:
            t = benchmark(cls, num_threads=n)
            print(f"{cls.__name__} with {n} threads: {t:.4f}s")
