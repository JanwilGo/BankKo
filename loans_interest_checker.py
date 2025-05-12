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
    with open("interest_checker_log.txt", "a", encoding='utf-8') as f:
        f.write(f"\n[Interest Checker] Running interest check at {datetime.now()}...\n")
    print(f"\n[Interest Checker] Running interest check at {datetime.now()}...")
    
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    
    # Get all active loans with their payment information and server time
    cursor.execute("""
        SELECT 
            l.*,
            COALESCE(SUM(lp.amount), 0) as total_paid,
            MAX(lp.paid_at) as last_payment_date,
            CURRENT_TIMESTAMP() as server_time,
            TIMESTAMPDIFF(DAY, 
                COALESCE(l.last_interest_applied, l.created_at),
                CURRENT_TIMESTAMP()
            ) as days_since_last_interest
        FROM loans l
        LEFT JOIN loan_payments lp ON l.loan_id = lp.loan_id
        WHERE l.status = 'debt'
        GROUP BY l.loan_id
    """)
    
    active_loans = cursor.fetchall()
    
    for loan in active_loans:
        print(f"\nProcessing loan {loan['loan_id']}:")
        print(f"- Created at: {loan['created_at']}")
        print(f"- Interest type: {loan['interest_type']}")
        print(f"- Interest rate: {loan['interest_rate']}%")
        print(f"- Principal: PHP {loan['principal']:,.2f}")
        print(f"- Current total due: PHP {loan['total_due']:,.2f}")
        print(f"- Total paid so far: PHP {loan['total_paid']:,.2f}")
        
        # Get the start point for interest calculation
        last_applied = loan['last_interest_applied'] or loan['created_at']
        server_now = loan['server_time']
        days_passed = loan['days_since_last_interest']
        
        print(f"- Last interest applied: {last_applied}")
        print(f"- Current server time: {server_now}")
        print(f"- Days passed since last interest: {days_passed}")
        
        # Calculate periods based on interest type
        if loan['interest_type'] == 'yearly':
            periods_passed = days_passed // 365
            period_length = 365
            rate = loan['interest_rate'] / 100
            print(f"- Yearly loan: {periods_passed} complete years passed")
            
        elif loan['interest_type'] == 'quarterly':
            periods_passed = days_passed // 91  # Using 91 days for quarters
            period_length = 91
            rate = loan['interest_rate'] / 100
            print(f"- Quarterly loan: {periods_passed} complete quarters passed")
        
        if periods_passed > 0:
            print(f"\nApplying {periods_passed} periods of interest:")
            
            # Calculate remaining amount after all payments
            remaining_due = max(loan['total_due'] - loan['total_paid'], 0)
            total_interest = 0
            
            print(f"- Original total due: PHP {loan['total_due']:,.2f}")
            print(f"- Amount paid so far: PHP {loan['total_paid']:,.2f}")
            print(f"- Remaining before interest: PHP {remaining_due:,.2f}")
            print(f"- Interest rate per period: {rate*100}%")
            
            # Apply compound interest for each period
            for i in range(periods_passed):
                interest = remaining_due * rate
                total_interest += interest
                remaining_due += interest
                print(f"  Period {i+1}: Interest: PHP {interest:,.2f}, Running total: PHP {remaining_due:,.2f}")
            
            # Calculate new total due
            new_total_due = loan['total_due'] + total_interest
            
            print(f"\nFinal calculations:")
            print(f"- Total interest added: PHP {total_interest:,.2f}")
            print(f"- New total due: PHP {new_total_due:,.2f}")
            
            # Calculate new last_interest_applied date using MySQL date functions
            cursor.execute("""
                UPDATE loans 
                SET total_due = %s,
                    last_interest_applied = DATE_ADD(
                        COALESCE(last_interest_applied, created_at),
                        INTERVAL %s DAY
                    )
                WHERE loan_id = %s
            """, (new_total_due, periods_passed * period_length, loan['loan_id']))
            conn.commit()
            
            print(f"Database updated successfully for loan {loan['loan_id']}")
            
            # Log the interest application
            with open("interest_checker_log.txt", "a", encoding='utf-8') as f:
                f.write(f"Applied {periods_passed} periods of interest to loan {loan['loan_id']}: +PHP {total_interest:,.2f}\n")
        
        else:
            print(f"Not enough time has passed for loan {loan['loan_id']} to apply interest")
    
    cursor.close()
    conn.close()
    print("\n[Interest Checker] Check completed")

def start_interest_checker():
    ensure_last_interest_column()
    print("[Interest Checker] Starting interest checker thread...")
    
    def check_periodically():
        while True:
            try:
                apply_interest()
            except Exception as e:
                print(f"[Interest Checker] Error: {e}")
                with open("interest_checker_log.txt", "a") as f:
                    f.write(f"[Interest Checker] Error: {e}\n")
            time.sleep(3600)  # Check every hour
    
    thread = threading.Thread(target=check_periodically, daemon=True)
    thread.start()
    print("[Interest Checker] Thread started")

if __name__ == "__main__":
    start_interest_checker()
    while True:
        time.sleep(10) 