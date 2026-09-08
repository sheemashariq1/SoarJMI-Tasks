import csv, os, heapq
from main import allocate, export_manifest

passed = 0
failed = 0

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

def make_students(n, start_hour=9):
    return [
        (f"2024-01-15 {start_hour + i // 60:02d}:{i % 60:02d}:00",
         f"Student{i}", f"s{i}@jmi.ac.in")
        for i in range(n)
    ]

def make_shuffled_students():
    return [
        ("2024-01-15 11:00:00", "Late Larry",  "larry@jmi.ac.in"),
        ("2024-01-15 09:00:00", "Early Emma",  "emma@jmi.ac.in"),
        ("2024-01-15 10:30:00", "Mid Mike",    "mike@jmi.ac.in"),
        ("2024-01-15 08:45:00", "First Faiz",  "faiz@jmi.ac.in"),
        ("2024-01-15 12:00:00", "Last Lisa",   "lisa@jmi.ac.in"),
    ]

run_test("TC1 - Capacity Underflow (30 students, cap=50)",
         make_students(30), 50, 30, 0)


run_test("TC2 - Capacity Overflow (70 students, cap=50)",
         make_students(70), 50, 50, 20)


run_test("TC3 - Exact Match (50 students, cap=50)",
         make_students(50), 50, 50, 0)

shuffled = make_shuffled_students()
confirmed, waitlist = allocate(shuffled, seat_cap=3)
expected_first = "First Faiz"
actual_first   = confirmed[0][1]
ok = actual_first == expected_first
status = "✅ PASS" if ok else "❌ FAIL"
if ok: passed += 1
else:  failed += 1
print(f"{status} | TC4 - Timestamp Priority (FCFS heap order)")
if not ok:
    print(f"       Expected first confirmed: {expected_first}, got: {actual_first}")

confirmed_data, waitlist_data = allocate(make_students(8), seat_cap=5)
export_manifest("test_manifest.csv", confirmed_data, waitlist_data)

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

import subprocess, sys
result = subprocess.run(
    [sys.executable, "main.py", "--cap", "3", "--input", "students.csv", "--output", "test_out.csv"],
    capture_output=True, text=True
)
cli_ok = result.returncode == 0 and os.path.exists("test_out.csv")
if cli_ok:
    with open("test_out.csv") as f:
        rows = list(csv.DictReader(f))
        cli_ok = rows[0]["status"] == "Confirmed" and len(rows) == 10
    os.remove("test_out.csv")

status = "✅ PASS" if cli_ok else "❌ FAIL"
if cli_ok: passed += 1
else:       failed += 1
print(f"{status} | TC6 - CLI --cap flag (python main.py --cap 3)")

print(f"\n{'─'*45}")
print(f"Results: {passed} passed, {failed} failed out of {passed+failed} tests")