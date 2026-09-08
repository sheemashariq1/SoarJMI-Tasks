# Task — Automated Event Seat Allocation Engine

**SoarJMI | Programming & DSA Task**

---

## What It Does

A backend algorithmic utility written in Python that manages event seat allocation and waitlists using a Min-Heap (Priority Queue). It reads student registration data from a CSV, allocates seats strictly on a first-come-first-served basis using timestamp ordering, and exports a unified attendee manifest to a single CSV file with a `status` column.

---

## How to Run

```bash
# Default (cap=5, input=students.csv, output=manifest.csv)
python main.py

# Custom seat cap
python main.py --cap 50

# Custom input/output files
python main.py --cap 50 --input input.csv --output output.csv
```

---

## CLI Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `--cap` | `5` | Seat capacity for the event |
| `--input` | `input.csv` | Input CSV file with registrations |
| `--output` | `output.csv` | Output attendee manifest CSV |

---

## Input Format — `input.csv`

Timestamps are manually entered to simulate real registration form data.

```
name,email,timestamp
Rahul Sharma,rahul@jmi.ac.in,2024-01-15 09:12:34
Priya Singh,priya@jmi.ac.in,2024-01-15 10:00:00
```

---

## Output — `output.csv`

A single unified attendee manifest with all registrants and their allocation status.

```
name,email,timestamp,status
Rahul Sharma,rahul@jmi.ac.in,2024-01-15 09:12:34,Confirmed
Priya Singh,priya@jmi.ac.in,2024-01-15 10:00:00,Waitlist
```

---

## Sample Output

```
========================================
       SEAT ALLOCATION SUMMARY
========================================
  Seat Capacity     : 5
  Total Registered  : 10
  Confirmed         : 5
  Waitlisted        : 5
========================================

  First seat     → Rahul Sharma (2024-01-15 09:12:34)
  First waitlist → Meera Nair  (2024-01-15 11:00:52)

  Manifest saved → manifest.csv
```

---

## Data Structure Used

### Min-Heap (`heapq`)

Each student is pushed as a tuple `(timestamp, name, email)`. Since Python compares tuples lexicographically, the earliest timestamp always sits at the top of the heap — guaranteeing FCFS (First Come, First Served) ordering without sorting the entire list upfront.

```python
heapq.heappush(heap, (timestamp, name, email))
ts, name, email = heapq.heappop(heap)  # always pops the earliest
```

---

## Time Complexity Analysis

| Operation | Complexity | Reason |
|-----------|------------|--------|
| `heappush` per student | O(log n) | Heap re-balances after each insert |
| `heappop` per student | O(log n) | Heap re-balances after each removal |
| Full allocation (n students) | **O(n log n)** | n pushes + n pops, each O(log n) |
| CSV read / write | O(n) | Single pass over n rows |
| **Overall** | **O(n log n)** | Dominated by heap operations |

**Space Complexity:** O(n) — all n students stored in the heap at once.

---

## Running Tests

```bash
python Test_Allocation.py
```

Covers 6 test cases: capacity underflow, overflow, exact match, timestamp priority, CSV export validation, and CLI flag verification.

---

## Submission

```
Task ID & Title:        Task 2.3 - Automated Event Seat Allocation Engine
Implementation Summary: Built a Python min-heap utility that reads student
                        registrations from CSV, allocates seats by timestamp
                        (FCFS), and exports a unified manifest CSV with status
                        column. Supports configurable seat cap and I/O files
                        via CLI arguments. Time complexity: O(n log n).
```