import heapq, csv, argparse, os

DEFAULT_SEAT_CAP = 5

def allocate(students_data, seat_cap):
    """
    Core allocation logic using a min-heap.
    Input:  list of (timestamp, name, email) tuples
    Output: (confirmed_list, waitlist_list) — both sorted by timestamp
    """
    heap = []
    for ts, name, email in students_data:
        heapq.heappush(heap, (ts, name, email))

    confirmed, waitlist = [], []
    while heap:
        ts, name, email = heapq.heappop(heap)
        if len(confirmed) < seat_cap:
            confirmed.append((ts, name, email))
        else:
            waitlist.append((ts, name, email))

    return confirmed, waitlist

def load_csv(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Input file '{filepath}' not found.")
    students = []
    with open(filepath) as f:
        for row in csv.DictReader(f):
            students.append((row["timestamp"], row["name"], row["email"]))
    return students

def export_manifest(filename, confirmed, waitlist):
    """Export a single unified attendee manifest CSV."""
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "email", "timestamp", "status"])
        for ts, name, email in confirmed:
            writer.writerow([name, email, ts, "Confirmed"])
        for ts, name, email in waitlist:
            writer.writerow([name, email, ts, "Waitlist"])

def print_summary(confirmed, waitlist, seat_cap):
    total = len(confirmed) + len(waitlist)
    print()
    print("=" * 40)
    print("       SEAT ALLOCATION SUMMARY")
    print("=" * 40)
    print(f"  Seat Capacity     : {seat_cap}")
    print(f"  Total Registered  : {total}")
    print(f"  Confirmed         : {len(confirmed)}")
    print(f"  Waitlisted        : {len(waitlist)}")
    print("=" * 40)
    if confirmed:
        print("\n  First seat →", confirmed[0][1], f"({confirmed[0][0]})")
    if waitlist:
        print("  First waitlist →", waitlist[0][1], f"({waitlist[0][0]})")
    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Event Seat Allocation Engine")
    parser.add_argument("--cap",    type=int, default=DEFAULT_SEAT_CAP,
                        help=f"Seat capacity (default: {DEFAULT_SEAT_CAP})")
    parser.add_argument("--input",  type=str, default="students.csv",
                        help="Input CSV file (default: students.csv)")
    parser.add_argument("--output", type=str, default="manifest.csv",
                        help="Output manifest CSV (default: manifest.csv)")
    args = parser.parse_args()

    students = load_csv(args.input)
    confirmed, waitlist = allocate(students, args.cap)

    export_manifest(args.output, confirmed, waitlist)
    print_summary(confirmed, waitlist, args.cap)

    print(f"  Manifest saved → {args.output}")
    print()