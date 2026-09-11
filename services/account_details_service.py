from database.connection import create_connection


class AccountDetailsService:

    @staticmethod
    def get_account_details(account_id):

        connection = create_connection()

        if connection is None:
            return None

        cursor = connection.cursor(dictionary=True)

        try:
            query = """
            SELECT
                c.customer_id,
                c.full_name,
                c.phone,
                c.email,
                c.address,
                c.created_at AS customer_created_at,

                a.account_id,
                a.account_number,
                a.account_type,
                a.balance,
                a.status,
                a.created_at AS account_created_at

            FROM customers c

            INNER JOIN accounts a
                ON c.customer_id = a.customer_id

            WHERE a.account_id = %s
            """

            cursor.execute(query, (account_id,))

            account_details = cursor.fetchone()

            return account_details

        except Exception as error:
            print("Failed to fetch account details:", error)
            return None

        finally:
            cursor.close()
            connection.close()