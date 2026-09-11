from database.connection import create_connection
from utils.security import hash_pin, verify_pin


class ChangePinService:

    @staticmethod
    def change_pin(account_id, current_pin, new_pin):

        connection = create_connection()

        if connection is None:
            return False

        cursor = connection.cursor()

        try:
            # Get the current PIN hash
            query = """
            SELECT pin_hash
            FROM accounts
            WHERE account_id = %s
            """

            cursor.execute(query, (account_id,))
            result = cursor.fetchone()

            if result is None:
                print("\nAccount not found.")
                return False

            stored_hash = result[0]

            # Verify current PIN
            if not verify_pin(current_pin, stored_hash):
                print("\nIncorrect current PIN.")
                return False

            # Hash the new PIN
            new_pin_hash = hash_pin(new_pin)

            # Update PIN
            update_query = """
            UPDATE accounts
            SET pin_hash = %s
            WHERE account_id = %s
            """

            cursor.execute(
                update_query,
                (new_pin_hash, account_id)
            )

            connection.commit()

            print("\n========================================")
            print("           PIN CHANGED SUCCESSFULLY")
            print("========================================")

            return True

        except Exception as error:
            connection.rollback()
            print("Failed to change PIN:", error)
            return False

        finally:
            cursor.close()
            connection.close()