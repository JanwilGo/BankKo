# BanKo - Banking Application

A modern banking application built with Python and Tkinter, featuring loan management, transactions, and automated interest calculations.

## Features

- **User Authentication**
  - Secure login and signup
  - Password hashing with bcrypt
  - Session management

- **Account Management**
  - View account balance
  - Transaction history
  - Profile management

- **Banking Operations**
  - Deposit funds
  - Withdraw money
  - Transfer between accounts

- **Loan System**
  - Apply for loans
    - Yearly simple interest loans
    - Quarterly simple interest loans
  - Automated interest calculations
  - Loan payment tracking
  - Payment history

- **Advanced Features**
  - Automated interest checker
  - Time travel functionality for testing
  - Real-time balance updates
  - Success notifications

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/JanwilGo/BankKo
   cd BankKo
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the code:
 1. Run the script:
   ```bash
   python login.py
   ```

### Testing the code:
  ## Time Travel 

- **Yearly**: Moves dates back by 366 days (leap year safe)
- **Quarterly**: Moves dates back by 92 days

## Loan Selection

- **All Loans**: Leave the Loan ID field empty
- **Single Loan**: Enter a specific loan ID

## Database Impact

The tool modifies two date fields in the loans table:
- `created_at`: Loan creation date
- `last_interest_applied`: Last interest calculation date

## Example Use Cases

1. **Testing Interest Calculations**
   - Move loans back in time to test interest accrual
   - Verify interest calculations for different loan ages

2. **System Testing**
   - Test how the system handles aged loans
   - Verify loan lifecycle processes

## Usage

1. Run the script:
   ```bash
   python loans_time_travel.py
   ```

2. In the GUI window:
   - Select time period (Yearly/Quarterly)
   - Optionally enter a specific loan ID
   - Click "Time Travel!"



## MySQL database DDL: (If you want to make an mysql db of your own)

CREATE TABLE loan_payments (
  payment_id int(11) NOT NULL AUTO_INCREMENT,
  loan_id int(11) NOT NULL,
  user_id int(11) NOT NULL,
  amount decimal(15,2) NOT NULL,
  paid_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (payment_id),
  KEY loan_id (loan_id),
  KEY user_id (user_id),
  CONSTRAINT loan_payments_ibfk_1 FOREIGN KEY (loan_id) REFERENCES loans (loan_id),
  CONSTRAINT loan_payments_ibfk_2 FOREIGN KEY (user_id) REFERENCES users (user_id)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=latin1


CREATE TABLE loans (
  loan_id int(11) NOT NULL AUTO_INCREMENT,
  user_id int(11) NOT NULL,
  principal decimal(15,2) NOT NULL,
  interest_rate decimal(5,2) NOT NULL,
  interest_type enum('yearly','quarterly') NOT NULL,
  total_due decimal(15,2) NOT NULL,
  status enum('debt','paid') NOT NULL DEFAULT 'debt',
  created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  paid_at timestamp NULL DEFAULT NULL,
  PRIMARY KEY (loan_id),
  KEY user_id (user_id),
  CONSTRAINT loans_ibfk_1 FOREIGN KEY (user_id) REFERENCES users (user_id)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1



CREATE TABLE transactions (
  transaction_id int(11) NOT NULL AUTO_INCREMENT,
  user_id int(11) NOT NULL,
  type enum('deposit','withdrawal','transfer') NOT NULL,
  amount decimal(15,2) NOT NULL,
  recipient_id int(11) DEFAULT NULL,
  created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (transaction_id),
  KEY user_id (user_id),
  CONSTRAINT transactions_ibfk_1 FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=latin1



CREATE TABLE users (
  user_id int(11) NOT NULL AUTO_INCREMENT,
  first_name varchar(50) NOT NULL,
  middle_initial char(1) DEFAULT NULL,
  family_name varchar(50) NOT NULL,
  email varchar(100) NOT NULL,
  password_hash varchar(255) NOT NULL,
  address text NOT NULL,
  phone_number varchar(15) NOT NULL,
  balance decimal(15,2) NOT NULL DEFAULT '0.00',
  created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (user_id),
  UNIQUE KEY email (email),
  UNIQUE KEY phone_number (phone_number)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1


## Acknowledgments

- Built with Python 3.13
- Uses Tkinter for GUI
- MySQL for database management
- Uses Bcrypt for encryption
- Lev
- JP
