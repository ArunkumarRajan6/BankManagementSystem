from database.connection import create_connection


class TransactionService:

    @staticmethod
    def get_transaction_history(account_id):

        connection = create_connection()

        if connection is None:
            return []

        cursor = connection.cursor(dictionary=True)

        try:
            query = """
            SELECT
                transaction_id,
                transaction_type,
                amount,
                balance_after,
                reference_number,
                description,
                transaction_date
            FROM transactions
            WHERE account_id = %s
            ORDER BY transaction_date DESC
            """

            cursor.execute(query, (account_id,))

            transactions = cursor.fetchall()

            return transactions

        except Exception as error:
            print("Failed to fetch transaction history:", error)
            return []

        finally:
            cursor.close()
            connection.close()