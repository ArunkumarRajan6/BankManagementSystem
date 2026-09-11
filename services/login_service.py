from database.connection import create_connection
from utils.security import verify_pin


class LoginService:

    @staticmethod
    def login(account_number, pin):

        connection = create_connection()

        if connection is None:
            return None

        cursor = connection.cursor(dictionary=True)

        try:
            query = """
            SELECT
                account_id,
                customer_id,
                account_number,
                account_type,
                balance,
                pin_hash,
                status
            FROM accounts
            WHERE account_number = %s
            """

            cursor.execute(query, (account_number,))

            account = cursor.fetchone()

            if account is None:
                print("\nAccount not found.")
                return "ACCOUNT_NOT_FOUND"

            if account["status"] != "Active":
                print("\nThis account is not active.")
                return None

            if not verify_pin(pin, account["pin_hash"]):
                return None

            print("\nLogin successful!")
            print(f"Welcome, Account {account['account_number']}")

            return account

        except Exception as error:
            print("Login failed:", error)
            return None

        finally:
            cursor.close()
            connection.close()