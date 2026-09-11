from database.connection import create_connection
import uuid


class WithdrawService:

    @staticmethod
    def withdraw(account_id, amount):

        connection = create_connection()

        if connection is None:
            return False

        cursor = connection.cursor()

        try:
            # Lock the account row while checking and updating balance
            query = """
            SELECT balance
            FROM accounts
            WHERE account_id = %s
            FOR UPDATE
            """

            cursor.execute(query, (account_id,))
            result = cursor.fetchone()

            if result is None:
                print("Account not found.")
                return False

            current_balance = result[0]

            # Check sufficient balance
            if current_balance < amount:
                print("\nInsufficient balance.")
                print(f"Available Balance: ₹{current_balance}")
                print(f"Requested Amount  : ₹{amount}")
                return False

            # Calculate new balance
            new_balance = current_balance - amount

            # Update account balance
            update_query = """
            UPDATE accounts
            SET balance = %s
            WHERE account_id = %s
            """

            cursor.execute(
                update_query,
                (new_balance, account_id)
            )

            # Generate transaction reference
            reference_number = (
                "TXN-" + uuid.uuid4().hex[:12].upper()
            )

            # Record withdrawal transaction
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
                    "WITHDRAW",
                    amount,
                    new_balance,
                    reference_number,
                    "Cash withdrawal"
                )
            )

            # Save both operations together
            connection.commit()

            print("\n========================================")
            print("         WITHDRAWAL SUCCESSFUL")
            print("========================================")
            print(f"Amount Withdrawn : ₹{amount}")
            print(f"New Balance      : ₹{new_balance}")
            print(f"Reference Number  : {reference_number}")
            print("========================================")

            return True

        except Exception as error:
            connection.rollback()
            print("Withdrawal failed:", error)
            return False

        finally:
            cursor.close()
            connection.close()