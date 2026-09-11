from database.connection import create_connection
from utils.security import hash_pin


class RegistrationService:

    @staticmethod
    def generate_account_number(cursor):
        import secrets

        while True:
            account_number = str(
                secrets.randbelow(9000000000) + 1000000000
            )

            query = """
            SELECT account_id
            FROM accounts
            WHERE account_number = %s
            """

            cursor.execute(query, (account_number,))

            if cursor.fetchone() is None:
                return account_number

    @staticmethod
    def register_customer(
        full_name,
        phone,
        email,
        address,
        account_type,
        initial_deposit,
        pin
    ):
        connection = create_connection()

        if connection is None:
            return None

        cursor = connection.cursor()

        try:
            # Step 1: Check whether phone already exists
            check_phone_query = """
            SELECT customer_id
            FROM customers
            WHERE phone = %s
            """

            cursor.execute(check_phone_query, (phone,))

            if cursor.fetchone():
                print("A customer with this phone number already exists.")
                return None

            # Step 2: Create customer
            customer_query = """
            INSERT INTO customers
            (full_name, phone, email, address)
            VALUES (%s, %s, %s, %s)
            """

            cursor.execute(
                customer_query,
                (full_name, phone, email, address)
            )

            customer_id = cursor.lastrowid

            # Step 3: Generate unique account number
            account_number = RegistrationService.generate_account_number(
                cursor
            )

            # Step 4: Hash PIN
            pin_hash = hash_pin(pin)

            # Step 5: Create account
            account_query = """
            INSERT INTO accounts
            (
                customer_id,
                account_number,
                account_type,
                balance,
                pin_hash
            )
            VALUES (%s, %s, %s, %s, %s)
            """

            cursor.execute(
                account_query,
                (
                    customer_id,
                    account_number,
                    account_type,
                    initial_deposit,
                    pin_hash
                )
            )

            account_id = cursor.lastrowid

            # Step 6: Record initial deposit
            if initial_deposit > 0:

                import uuid

                reference_number = "TXN-" + uuid.uuid4().hex[:12].upper()

                transaction_query = """
                INSERT INTO transactions
                (
                    account_id,
                    transaction_type,
                    amount,
                    balance_after,
                    reference_number,
                    description
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                """

                cursor.execute(
                    transaction_query,
                    (
                        account_id,
                        "DEPOSIT",
                        initial_deposit,
                        initial_deposit,
                        reference_number,
                        "Initial account deposit"
                    )
                )

            # Step 7: Save everything
            connection.commit()

            print("\n========================================")
            print("       ACCOUNT CREATED SUCCESSFULLY")
            print("========================================")
            print(f"Customer ID    : {customer_id}")
            print(f"Account Number : {account_number}")
            print(f"Account Type   : {account_type}")
            print(f"Initial Deposit: ₹{initial_deposit}")
            print("========================================")

            return {
                "customer_id": customer_id,
                "account_id": account_id,
                "account_number": account_number
            }

        except Exception as error:
            connection.rollback()
            print("Registration failed:", error)
            return None

        finally:
            cursor.close()
            connection.close()