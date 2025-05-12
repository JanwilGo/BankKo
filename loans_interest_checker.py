import threading
import time
import mysql.connector
from datetime import datetime, timedelta

DB_CONFIG = {
    'host': 'sql12.freesqldatabase.com',
    'user': 'sql12773881',
    'password': 'isUcpBumwQ',
    'database': 'sql12773881',
    'port': 3306
}

print("[Interest Checker] Module imported")

def ensure_last_interest_column():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SHOW COLUMNS FROM loans LIKE 'last_interest_applied'")
    if not cursor.fetchone():
        cursor.execute("ALTER TABLE loans ADD COLUMN last_interest_applied TIMESTAMP NULL DEFAULT NULL")
        conn.commit()
    cursor.close()
    conn.close()

def apply_interest():
    with open("interest_checker_log.txt", "a") as f:
        f.write("[Interest Checker] Running interest check...\n")
    print("[Interest Checker] Running interest check...")
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    now = datetime.now()
    cursor.execute("SELECT * FROM loans WHERE status = 'debt'")
    for loan in cursor.fetchall():
        last_applied = loan['last_interest_applied'] or loan['created_at']
        print(f"Checking loan {loan['loan_id']}: last_applied={last_applied}, now={now}, interest_type={loan['interest_type']}, total_due={loan['total_due']}")
        if loan['interest_type'] == 'yearly':
            period = timedelta(days=365)
            rate = loan['interest_rate'] / 100
        elif loan['interest_type'] == 'quarterly':
            period = timedelta(days=91)
            rate = loan['interest_rate'] / 100
        else:
            print(f"Loan {loan['loan_id']} has unknown interest_type: {loan['interest_type']}")
            continue
        if now - last_applied >= period:
            print(f"Applying interest to loan {loan['loan_id']}")
            cursor2 = conn.cursor()
            cursor2.execute("SELECT COALESCE(SUM(amount), 0) FROM loan_payments WHERE loan_id = %s", (loan['loan_id'],))
            paid = cursor2.fetchone()[0]
            cursor2.close()
            remaining_due = max(loan['total_due'] - paid, 0)
            interest = remaining_due * rate
            new_total_due = loan['total_due'] + interest
            print(f"Loan {loan['loan_id']} - paid: {paid}, remaining_due: {remaining_due}, interest: {interest}, new_total_due: {new_total_due}")
            cursor.execute("UPDATE loans SET total_due = %s, last_interest_applied = %s WHERE loan_id = %s", (new_total_due, now, loan['loan_id']))
            conn.commit()
        else:
            print(f"Not enough time has passed for loan {loan['loan_id']}")
    cursor.close()
    conn.close()

def interest_checker_thread():
    print("[Interest Checker] Thread started!")
    ensure_last_interest_column()
    while True:
        apply_interest()
        time.sleep(60)  # 1 minute

def start_interest_checker():
    print("[Interest Checker] start_interest_checker() called")
    t = threading.Thread(target=interest_checker_thread, daemon=True)
    t.start()

if __name__ == "__main__":
    start_interest_checker()
    while True:
        time.sleep(10) 