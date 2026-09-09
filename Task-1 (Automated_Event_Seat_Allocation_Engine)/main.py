# Importing required libraries
import heapq, csv, argparse, os

# Default seat capacity
DEFAULT_SEAT_CAP = 5

# This is the Core logic of the Seat Allocation Engine
# It returns two lists: confirmed and waitlist based on the seat capacity
def allocate(students_data, seat_cap):
    heap = []
    for ts, name, email in students_data:
        heapq.heappush(heap, (ts, name, email)) # Using a min-heap to sort students by timestamp

    confirmed, waitlist = [], []
    while heap:
        ts, name, email = heapq.heappop(heap) # Pop the student with the earliest timestamp from the heap
        if len(confirmed) < seat_cap:
            confirmed.append((ts, name, email)) # Add to confirmed list if seat capacity is not reached
        else:
            waitlist.append((ts, name, email)) # Add to waitlist if seat capacity is reached

    return confirmed, waitlist

# This opens the input CSV file and loads the data into a list of tuples (timestamp, name, email)
def load_csv(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Input file '{filepath}' not found.")
    students = []
    with open(filepath) as f:
        for row in csv.DictReader(f):  # Using DictReader to read CSV rows as dictionaries
            students.append((row["timestamp"], row["name"], row["email"]))
    return students

# This creates the output.csv file with the confirmed and waitlisted students as status
def export_output(filename, confirmed, waitlist):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "email", "timestamp", "status"])
        for ts, name, email in confirmed:
            writer.writerow([name, email, ts, "Confirmed"])
        for ts, name, email in waitlist:
            writer.writerow([name, email, ts, "Waitlist"])

# This prints the summary of the seat allocation process and output in the terminal
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

# Main function to handle command-line arguments and execute the seat allocation process
# argparse is used to parse command-line arguments such as --cap, --input, and --output

if __name__ == "__main__": # Ensures that the following code runs only on the main script execution and not when imported as a module
    parser = argparse.ArgumentParser(description="Event Seat Allocation Engine")
    parser.add_argument("--cap",    type=int, default=DEFAULT_SEAT_CAP,
                        help=f"Seat capacity (default: {DEFAULT_SEAT_CAP})")
    parser.add_argument("--input",  type=str, default="input.csv",
                        help="Input CSV file (default: input.csv)")
    parser.add_argument("--output", type=str, default="output.csv",
                        help="Output manifest CSV (default: output.csv)")
    args = parser.parse_args() # Parsing command-line arguments

    students = load_csv(args.input)
    confirmed, waitlist = allocate(students, args.cap)

    export_output(args.output, confirmed, waitlist)
    print_summary(confirmed, waitlist, args.cap)

    print(f"  Manifest saved → {args.output}")
    print()