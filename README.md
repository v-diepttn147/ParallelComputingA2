# PARALLEL COMPUTING COURSE
- Parallel Computing Course - HCMUT - 242
- Tran Thi Ngoc Diep - 2270711
- Mai Hong Quoc Khanh - 2270587
- Hardware 1: Apple M3 8 cores, 16GB
- Hardware 2: Windows 11, Intel® Core™ i5-12400F (12 CPUs), ~2.5GHz, 16GB 
## Assignment 2
### Setup Environments

#### Result: Sequential A*

The following table shows the result of sequential A* finding shortest path from Thu Duc Market to Ben Thanh Market.

| Hardware | Sequential A* (s) | Distance diff. (%) |
|----------|-------------------|--------------------|
| 1        | 0.65              | 1.29               |
| 2        | 0.35              | 1.20               |


### Concurrent Set Data Structure
### Problem Description

This task focuses on implementing and evaluating two concurrent variants of a sorted linked list used as a **set data structure**. Each variant applies a different synchronization strategy:

1. **Coarse-Grained Locking**: Locks the entire list for every operation.
2. **Fine-Grained Locking**: Locks individual nodes during traversal and update.

The objectives are:
- Ensure correctness under multi-threaded access.
- Compare performance under concurrent workloads.
- Optionally apply **exponential backoff** to reduce contention.

---

### Design & Implementation

#### 1. `CoarseGrainedSet`
- A global lock is used to protect the whole list.
- Simple to implement but has low concurrency.

#### 2. `FineGrainedSet`
- Each node contains its own lock.
- Threads only lock necessary parts of the list, allowing more parallelism.

Both classes support:
- `add(value)`
- `remove(value)`
- `contains(value)`

---

### Correctness Testing

We created a file `test_correctness.py` to:
- Simulate thousands of random operations (`add`, `remove`, `contains`) across 8 threads.
- Compare against a built-in Python `set` to verify correctness.
- Output number of passed test cases and detect inconsistencies if any.

Test Cases:
- **Test Case 1**: Add elements and verify with `contains()`.
- **Test Case 2**: Remove elements and verify they no longer exist.
- **Test Case 3**: Multi-threaded `add/remove` with `contains()` checks for consistency.

All tests passed successfully.

---

### Performance Benchmark

The `benchmark.py` script runs randomized workloads with varying numbers of threads (1, 2, 4, 8). Each thread performs 5000 operations. Time taken is recorded for both variants.

#### Benchmark Results

| Variant           | Threads | Time (s) - Hardware 1 | Time (s) - Hardware 2 |
|------------------|---------|-----------------------|-----------------------|
| CoarseGrainedSet | 1       | -                     | 0.0446                |
| CoarseGrainedSet | 2       | -                     | 0.1099                |
| CoarseGrainedSet | 4       | -                     | 0.2358                |
| CoarseGrainedSet | 8       | -                     | 0.4632                |
| FineGrainedSet   | 1       | -                     | 0.0588                |
| FineGrainedSet   | 2       | -                     | 0.1484                |
| FineGrainedSet   | 4       | -                     | 0.3620                |
| FineGrainedSet   | 8       | -                     | 0.8729                |

**Observation**: Fine-grained locking outperforms coarse-grained locking under high concurrency.