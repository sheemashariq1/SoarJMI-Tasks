# Importing necessary libraries for CSV handling, file operations, and heap operations
import csv, os, heapq

# From main.py, importing the allocate and export_output functions
from main import allocate, export_output

# passed and failed counters to keep track of test results
passed = 0
failed = 0

# This is a reusable helper function to run a test case for the allocate function. It takes the test name, student data, seat capacity, and expected confirmed and waitlist counts as input.
def run_test(name, students_data, seat_cap, expect_confirmed, expect_waitlist):
    global passed, failed
    confirmed, waitlist = allocate(students_data, seat_cap)
    ok = len(confirmed) == expect_confirmed and len(waitlist) == expect_waitlist
    status = "✅ PASS" if ok else "❌ FAIL"
    if ok: passed += 1 
    else:  failed += 1
    print(f"{status} | {name}")
    if not ok:
        print(f"Expected confirmed={expect_confirmed}, waitlist={expect_waitlist}")
        print(f"Got     confirmed={len(confirmed)}, waitlist={len(waitlist)}")

# This function generates a fake list of student tuples with timestamps, names, and email addresses for testing purposes.
def make_students(n, start_hour=9):
    students = []
    for i in range(n):
        hour = start_hour + i // 60
        minute = i % 60
        timestamp = f"2024-01-15 {hour:02d}:{minute:02d}:00"
        name = f"Student{i}"
        email = f"s{i}@jmi.ac.in"
        students.append((timestamp, name, email))

    return students

# This function generates a shuffled list of student tuples to test the timestamp priority (FCFS) logic of the allocation engine.
def make_shuffled_students():
    return [
        ("2024-01-15 11:00:00", "Larry",  "larry@jmi.ac.in"),
        ("2024-01-15 09:00:00", "Emma",  "emma@jmi.ac.in"),
        ("2024-01-15 10:30:00", "Ayesha", "ayesha@jmi.ac.in"),
        ("2024-01-15 08:45:00", "Faiz", "faiz@jmi.ac.in"),
        ("2024-01-15 12:00:00", "Aman", "aman@jmi.ac.in"),
    ]

# Running the test cases for the allocate function with different scenarios

# Test Case 1: Capacity Underflow - 30 students, seat capacity = 50
run_test("TC1 - Capacity Underflow (30 students, cap=50)",
         make_students(30), 50, 30, 0)

# Test Case 2: Capacity Overflow - 70 students, seat capacity = 50
run_test("TC2 - Capacity Overflow (70 students, cap=50)",
         make_students(70), 50, 50, 20)

# Test Case 3: Exact Match - 50 students, seat capacity = 50
run_test("TC3 - Exact Match (50 students, cap=50)",
         make_students(50), 50, 50, 0)

# Test Case 4: Timestamp Priority (FCFS) - 5 students, seat capacity = 3
shuffled = make_shuffled_students()
confirmed, waitlist = allocate(shuffled, seat_cap=3)
expected_first = "Faiz" 
actual_first   = confirmed[0][1] # Get the name of the first confirmed student
ok = actual_first == expected_first
status = "✅ PASS" if ok else "❌ FAIL"
if ok: passed += 1
else:  failed += 1
print(f"{status} | TC4 - Timestamp Priority (FCFS heap order)")
if not ok:
    print(f"       Expected first confirmed: {expected_first}, got: {actual_first}")

# Test Case 5: Unified Manifest CSV - Check if the output CSV has correct columns, row count, and status values
confirmed_data, waitlist_data = allocate(make_students(8), seat_cap=5)
export_output("test_manifest.csv", confirmed_data, waitlist_data)

csv_ok = True
with open("test_manifest.csv") as f:
    rows = list(csv.DictReader(f))
    if len(rows) != 8:
        csv_ok = False
    statuses = [r["status"] for r in rows]
    if statuses.count("Confirmed") != 5 or statuses.count("Waitlist") != 3:
        csv_ok = False
    for row in rows:
        if not all(k in row for k in ["name", "email", "timestamp", "status"]):
            csv_ok = False
os.remove("test_manifest.csv")

status = "✅ PASS" if csv_ok else "❌ FAIL"
if csv_ok: passed += 1
else:       failed += 1
print(f"{status} | TC5 - Unified Manifest CSV (columns, row count, status values)")

# Test Case 6: Check that the CLI creates the output CSV with 3 seats and the expected allocation results.
import subprocess, sys

result = subprocess.run(
    [sys.executable, "main.py", "--cap", "3", "--input", "input.csv", "--output", "test_out.csv"],
    capture_output=True, text=True
)  # Run main.py with the specified arguments and capture its output and return code

check = result.returncode == 0 and os.path.exists("test_out.csv") # Check that the command executed successfully and the output file exists
if check:
    with open("test_out.csv") as f:
        rows = list(csv.DictReader(f))
        # Check that exactly 3 students are confirmed 
        confirmed_count = sum(1 for row in rows if row["status"] == "Confirmed")
        # Check that the remaining are on the waitlist
        waitlist_count = sum(1 for row in rows if row["status"] == "Waitlist")
        # Total should equal input file size
        check = confirmed_count == 3 and waitlist_count == len(rows) - 3
    os.remove("test_out.csv")

status = "✅ PASS" if check else "❌ FAIL"
if check: passed += 1
else: failed += 1
print(f"{status} | TC6 - CLI --cap flag (exactly 3 confirmed, rest waitlist)")

print(f"\n{'─'*45}")    # Separator for clarity in output
print(f"Results: {passed} passed, {failed} failed out of {passed+failed} tests")  # Summary of test results