from database.connection import create_connection

def create_tables():
    connection = create_connection()

    if connection is None:
        return

    cursor = connection.cursor()

    # 1. Customers table
    customers_table = """
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INT PRIMARY KEY AUTO_INCREMENT,
        full_name VARCHAR(100) NOT NULL,
        phone VARCHAR(15) NOT NULL UNIQUE,
        email VARCHAR(100) UNIQUE,
        address VARCHAR(255),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """

    # 2. Accounts table
    accounts_table = """
    CREATE TABLE IF NOT EXISTS accounts (
        account_id INT PRIMARY KEY AUTO_INCREMENT,
        customer_id INT NOT NULL,
        account_number VARCHAR(20) NOT NULL UNIQUE,
        account_type VARCHAR(20) NOT NULL DEFAULT 'Savings',
        balance DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
        pin_hash VARCHAR(255) NOT NULL,
        status VARCHAR(20) NOT NULL DEFAULT 'Active',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        CONSTRAINT fk_accounts_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
    )
    """

    # 3. Transactions table
    transactions_table = """
    CREATE TABLE IF NOT EXISTS transactions (
        transaction_id INT PRIMARY KEY AUTO_INCREMENT,
        account_id INT NOT NULL,
        transaction_type VARCHAR(30) NOT NULL,
        amount DECIMAL(15, 2) NOT NULL,
        balance_after DECIMAL(15, 2) NOT NULL,
        reference_number VARCHAR(50) NOT NULL UNIQUE,
        description VARCHAR(255),
        transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        CONSTRAINT fk_transactions_account
        FOREIGN KEY (account_id)
        REFERENCES accounts(account_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
    )
    """

    # 4. Beneficiaries table
    beneficiaries_table = """
    CREATE TABLE IF NOT EXISTS beneficiaries (
        beneficiary_id INT PRIMARY KEY AUTO_INCREMENT,
        account_id INT NOT NULL,
        beneficiary_account_number VARCHAR(20) NOT NULL,
        beneficiary_name VARCHAR(100) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        CONSTRAINT fk_beneficiary_account
        FOREIGN KEY (account_id)
        REFERENCES accounts(account_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
    )
    """

    try:
        cursor.execute(customers_table)
        cursor.execute(accounts_table)
        cursor.execute(transactions_table)
        cursor.execute(beneficiaries_table)

        connection.commit()

        print("Database tables created successfully.")

    except Exception as error:
        connection.rollback()
        print("Failed to create tables:", error)

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    create_tables()