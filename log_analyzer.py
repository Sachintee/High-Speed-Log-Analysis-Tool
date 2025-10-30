import sqlite3
import re
import os
import time
import multiprocessing as mp
from functools import partial

# --- GLOBAL CONFIGURATION ---
LOG_FILE = "sample_access.log"
DB_FILE = "log_data.db"

# A simplified regular expression pattern to parse a basic log line:
# IP - - [Timestamp] "Method URL Protocol" Status_Code Size
LOG_PATTERN = re.compile(r'^(\S+) \S+ \S+ \[([^\]]+)\] "(\S+) (\S+) \S+" (\d+) (\S+)$')

# --- ALGORITHMS COMPONENT ---
def run_optimized_analysis(conn):
    """
    Executes the optimized query to find the top 10 most frequent IP addresses.
    The efficiency of this step relies on the B-tree Index created on the IP_Address column.
    """
    print("\n--- Running Optimized Analysis (Algorithms) ---")
    start_time = time.time()
    cursor = conn.cursor()

    # Optimized SQL Query
    query = """
    SELECT IP_Address, COUNT(IP_Address) as RequestCount
    FROM Log_Entries
    GROUP BY IP_Address
    ORDER BY RequestCount DESC
    LIMIT 10;
    """
    try:
        cursor.execute(query)
        top_ips = cursor.fetchall()

        print(f"Analysis Time: {time.time() - start_time:.4f} seconds")
        print("\nTOP 10 MOST FREQUENT IP ADDRESSES:")
        for ip, count in top_ips:
            print(f"- {ip}: {count} requests")
    except sqlite3.OperationalError as e:
        print(f"Error executing analysis query: {e}. Ensure the database is loaded.")


# --- 2. ADVANCED DATABASE MANAGEMENT SYSTEM COMPONENT ---
def setup_database():
    """Sets up the SQLite database and creates the necessary table with an index."""
    print(f"--- Setting up Database ({DB_FILE}) and Indexing (DBMS) ---")
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Create the table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Log_Entries (
        LogID INTEGER PRIMARY KEY AUTOINCREMENT,
        IP_Address TEXT NOT NULL,
        Timestamp TEXT,
        Method TEXT,
        URL TEXT,
        Status_Code INTEGER
    );
    """)

    # Create an Index on IP_Address for fast querying (crucial for the optimized analysis)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_ip ON Log_Entries (IP_Address);")
    conn.commit()
    return conn

def bulk_load_data(conn, parsed_data):
    """Loads parsed data into the database using bulk insertion (executemany)."""
    print(f"Loading {len(parsed_data)} records into the database...")
    cursor = conn.cursor()
    cursor.executemany(
        "INSERT INTO Log_Entries (IP_Address, Timestamp, Method, URL, Status_Code) VALUES (?, ?, ?, ?, ?)",
        parsed_data
    )
    conn.commit()
    print("Bulk loading complete.")

# --- 3. PYTHON PROGRAMMING & PARSING LOGIC ---
def parse_log_line(line):
    """Parses a single log line using the defined regex."""
    match = LOG_PATTERN.match(line)
    if match:
        return (match.group(1), match.group(2), match.group(3), match.group(4), int(match.group(5)))
    return None

def generate_sample_log(num_lines):
    """Creates a simple log file for testing."""
    if os.path.exists(LOG_FILE):
        print(f"Existing log file '{LOG_FILE}' found. Skipping generation.")
        return

    print(f"Generating a sample log file with {num_lines} lines...")
    common_ips = ["192.168.1.1", "10.0.0.5", "172.16.0.2", "173.15.2.1", "192.162.1.1", "10.1.0.1", "152.63.8.1", "192.123.0.1", "198.33.0.0", "8.1.8.8", "9.8.0.0", "11.1.11.1", "192.68.1.1", "198.15.2.1", "198.63.1.1", "147.56.2.0", "123.69.1.1", "196.153.78.1"] # Added one more IP
    common_urls = ["/home", "/product/view", "/about", "/api/data", "/images/logo.png"]
    status_codes = [200, 200, 200, 404, 500, 200]

    with open(LOG_FILE, 'w') as f:
        for i in range(num_lines):
            ip = common_ips[i % len(common_ips)]
            url = common_urls[i % len(common_urls)]
            status = status_codes[i % len(status_codes)]
            timestamp = time.strftime("%d/%b/%Y:%H:%M:%S +0000", time.localtime(time.time() - i))
            line = f'{ip} - - [{timestamp}] "GET {url} HTTP/1.1" {status} 1024\n'
            f.write(line)
    print("Sample log generation complete.")

# --- 4. HIGH PERFORMANCE COMPUTING COMPONENT ---
def process_log_data_parallel(file_path):
    """Uses multiprocessing to parse lines concurrently."""
    print("\n--- Starting Parallel Log Parsing (HPC) ---")
    start_time = time.time()

    try:
        with open(file_path, 'r') as f:
            log_lines = f.readlines()
    except FileNotFoundError:
        print(f"ERROR: Log file '{file_path}' not found.")
        return []

    num_cores = mp.cpu_count()
    print(f"Using {num_cores} cores for parallel processing.")

    with mp.Pool(num_cores) as pool:
        parsed_data_list = list(filter(None, pool.map(parse_log_line, log_lines)))

    end_time = time.time()
    print(f"Parallel Parsing Time: {end_time - start_time:.4f} seconds")
    return parsed_data_list


# --- MAIN EXECUTION FLOW ---
def main():
    """Orchestrates the entire log analysis pipeline."""
    # Step 0: Ensure the log file exists
    generate_sample_log(num_lines=10000)

    # Step 1: Setup the Database (DBMS)
    conn = setup_database()

    # Step 2: Process Log Data in Parallel (HPC)
    parsed_records = process_log_data_parallel(LOG_FILE)

    if not parsed_records:
        conn.close()
        return

    # Step 3: Bulk Load Data into the DB (DBMS Optimization)
    bulk_load_data(conn, parsed_records)

    # Step 4: Run Optimized Analysis (Algorithms)
    run_optimized_analysis(conn)

    # Clean up
    conn.close()
    print("\nProject execution finished successfully.")

if __name__ == "__main__":
    main()
