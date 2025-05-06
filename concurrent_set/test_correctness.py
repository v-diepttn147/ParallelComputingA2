from coarse_grained_set import CoarseGrainedSet
from fine_grained_set import FineGrainedSet
import threading
import random

def run_add_test(set_class):
    print(f"\nTest Case 1: add() correctness")

    s = set_class()
    test_values = list(range(1, 101))

    for val in test_values:
        s.add(val)

    # Kiểm tra
    passed = 0
    for val in test_values:
        if s.contains(val):
            passed += 1
        else:
            print(f"FAIL: add({val}) → not found")
    print(f"PASSED: {passed}/{len(test_values)} values found after add()")

def run_remove_test(set_class):
    print(f"\nTest Case 2: remove() correctness")

    s = set_class()
    test_values = list(range(1, 101))
    for val in test_values:
        s.add(val)

    for val in test_values:
        s.remove(val)

    # Kiểm tra
    passed = 0
    for val in test_values:
        if not s.contains(val):
            passed += 1
        else:
            print(f"FAIL: remove({val}) → still found")
    print(f"PASSED: {passed}/{len(test_values)} values correctly removed")

def run_contains_test(set_class):
    print(f"\nTest Case 3: contains() random check under multi-thread")

    s = set_class()
    reference = set()
    lock = threading.Lock()
    NUM_THREADS = 4

    def worker():
        for _ in range(1000):
            val = random.randint(1, 50)
            op = random.choice(['add', 'remove'])
            if op == 'add':
                s.add(val)
                with lock:
                    reference.add(val)
            else:
                s.remove(val)
                with lock:
                    reference.discard(val)

    threads = [threading.Thread(target=worker) for _ in range(NUM_THREADS)]
    for t in threads: t.start()
    for t in threads: t.join()

    passed = 0
    for val in range(1, 51):
        if s.contains(val) == (val in reference):
            passed += 1
        else:
            print(f"FAIL: contains({val}) mismatch")
    print(f"PASSED: {passed}/50 random contains() values matched")

def run_all_tests(set_class, class_name):
    print(f"\n============================")
    print(f"Running tests for: {class_name}")
    print(f"============================")

    run_add_test(set_class)
    run_remove_test(set_class)
    run_contains_test(set_class)

if __name__ == "__main__":
    run_all_tests(CoarseGrainedSet, "CoarseGrainedSet")
    run_all_tests(FineGrainedSet, "FineGrainedSet")
