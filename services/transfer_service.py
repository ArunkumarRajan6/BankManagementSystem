from database.connection import create_connection
import uuid


class TransferService:

    @staticmethod
    def transfer(sender_account_id, receiver_account_number, amount):

        connection = create_connection()

        if connection is None:
            return False

        cursor = connection.cursor(dictionary=True)

        try:
            # Get receiver account
            receiver_query = """
            SELECT
                account_id,
                account_number,
                balance,
                status
            FROM accounts
            WHERE account_number = %s
            """

            cursor.execute(
                receiver_query,
                (receiver_account_number,)
            )

            receiver = cursor.fetchone()

            if receiver is None:
                print("\nReceiver account not found.")
                return False

            # Prevent transferring to the same account
            if receiver["account_id"] == sender_account_id:
                print("\nYou cannot transfer money to your own account.")
                return False

            # Check receiver status
            if receiver["status"] != "Active":
                print("\nReceiver account is not active.")
                return False

            # Lock sender and receiver rows
            if sender_account_id < receiver["account_id"]:
                first_id = sender_account_id
                second_id = receiver["account_id"]
            else:
                first_id = receiver["account_id"]
                second_id = sender_account_id

            lock_query = """
            SELECT
                account_id,
                balance,
                status
            FROM accounts
            WHERE account_id IN (%s, %s)
            ORDER BY account_id
            FOR UPDATE
            """

            cursor.execute(
                lock_query,
                (first_id, second_id)
            )

            locked_accounts = cursor.fetchall()

            if len(locked_accounts) != 2:
                print("\nUnable to lock both accounts.")
                return False

            sender = None
            receiver_locked = None

            for account in locked_accounts:
                if account["account_id"] == sender_account_id:
                    sender = account

                elif account["account_id"] == receiver["account_id"]:
                    receiver_locked = account

            if sender is None or receiver_locked is None:
                print("\nUnable to retrieve account information.")
                return False

            # Check sender status
            if sender["status"] != "Active":
                print("\nYour account is not active.")
                return False

            # Check sufficient balance
            if sender["balance"] < amount:
                print("\nInsufficient balance.")
                print(f"Available Balance: ₹{sender['balance']}")
                print(f"Transfer Amount  : ₹{amount}")
                return False

            # Calculate new balances
            sender_new_balance = sender["balance"] - amount
            receiver_new_balance = receiver_locked["balance"] + amount

            # Update sender balance
            sender_update_query = """
            UPDATE accounts
            SET balance = %s
            WHERE account_id = %s
            """

            cursor.execute(
                sender_update_query,
                (
                    sender_new_balance,
                    sender_account_id
                )
            )

            # Update receiver balance
            receiver_update_query = """
            UPDATE accounts
            SET balance = %s
            WHERE account_id = %s
            """

            cursor.execute(
                receiver_update_query,
                (
                    receiver_new_balance,
                    receiver["account_id"]
                )
            )

            # Generate separate transaction references
            sender_reference = (
                "TXN-" + uuid.uuid4().hex[:12].upper()
            )

            receiver_reference = (
                "TXN-" + uuid.uuid4().hex[:12].upper()
            )

            # Sender transaction
            sender_transaction_query = """
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
                sender_transaction_query,
                (
                    sender_account_id,
                    "TRANSFER_OUT",
                    amount,
                    sender_new_balance,
                    sender_reference,
                    f"Transfer to {receiver['account_number']}"
                )
            )

            # Receiver transaction
            receiver_transaction_query = """
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
                receiver_transaction_query,
                (
                    receiver["account_id"],
                    "TRANSFER_IN",
                    amount,
                    receiver_new_balance,
                    receiver_reference,
                    f"Transfer from account {sender_account_id}"
                )
            )

            # Save everything together
            connection.commit()

            print("\n========================================")
            print("          TRANSFER SUCCESSFUL")
            print("========================================")
            print(f"Amount Transferred : ₹{amount}")
            print(f"To Account         : {receiver['account_number']}")
            print(f"New Balance        : ₹{sender_new_balance}")
            print(f"Reference Number   : {sender_reference}")
            print("========================================")

            return True

        except Exception as error:
            connection.rollback()
            print("Transfer failed:", error)
            return False

        finally:
            cursor.close()
            connection.close()