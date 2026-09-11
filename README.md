# Bank Management System

A console-based Bank Management System built using Python and MySQL.

## Features

- Customer registration
- Bank account creation
- Secure PIN-based login
- PIN validation and change PIN
- Balance checking
- Deposit money
- Withdraw money
- Money transfer
- Transaction history
- Beneficiary management
- Account details
- Input validation
- Database transactions with commit and rollback
- Secure PIN hashing using PBKDF2
- Environment variables for database credentials

## Technologies Used

- Python
- MySQL
- MySQL Connector/Python
- python-dotenv
- Object-Oriented Programming
- SQL
- Git & GitHub

## Project Structure

```text
BankManagementSystem/
│
├── database/
│   ├── _init_.py
│   ├── connection.py
│   └── setup.py
│
├── models/
│   ├── _init_.py
│   ├── customer.py
│   └── account.py
│
├── services/
│   ├── _init_.py
│   ├── account_details_service.py
│   ├── beneficiary_service.py
│   ├── change_pin_service.py
│   ├── customer_service.py
│   ├── deposit_service.py
│   ├── login_service.py
│   ├── registration_service.py
│   ├── transaction_service.py
│   ├── transfer_service.py
│   └── withdraw_service.py
│
├── utils/
│   ├── _init_.py
│   ├── security.py
│   └── validators.py
│
├── .env
├── .gitignore
├── main.py
├── README.md
└── requirements.txt