from database.connection import create_connection


class BeneficiaryService:

    @staticmethod
    def add_beneficiary(
        account_id,
        beneficiary_account_number,
        beneficiary_name
    ):
        connection = create_connection()

        if connection is None:
            return False

        cursor = connection.cursor(dictionary=True)

        try:
            # Check whether beneficiary account exists
            account_query = """
            SELECT account_id, account_number, status
            FROM accounts
            WHERE account_number = %s
            """

            cursor.execute(
                account_query,
                (beneficiary_account_number,)
            )

            beneficiary_account = cursor.fetchone()

            if beneficiary_account is None:
                print("\nBeneficiary account not found.")
                return False

            # Prevent adding own account
            if beneficiary_account["account_id"] == account_id:
                print("\nYou cannot add your own account as a beneficiary.")
                return False

            # Check whether beneficiary is already added
            duplicate_query = """
            SELECT beneficiary_id
            FROM beneficiaries
            WHERE account_id = %s
            AND beneficiary_account_number = %s
            """

            cursor.execute(
                duplicate_query,
                (
                    account_id,
                    beneficiary_account_number
                )
            )

            if cursor.fetchone() is not None:
                print("\nThis beneficiary is already added.")
                return False

            # Check beneficiary account status
            if beneficiary_account["status"] != "Active":
                print("\nBeneficiary account is not active.")
                return False

            # Insert beneficiary
            insert_query = """
            INSERT INTO beneficiaries
            (
                account_id,
                beneficiary_account_number,
                beneficiary_name
            )
            VALUES (%s, %s, %s)
            """

            cursor.execute(
                insert_query,
                (
                    account_id,
                    beneficiary_account_number,
                    beneficiary_name
                )
            )

            connection.commit()

            beneficiary_id = cursor.lastrowid

            print("\n========================================")
            print("       BENEFICIARY ADDED SUCCESSFULLY")
            print("========================================")
            print(f"Beneficiary ID    : {beneficiary_id}")
            print(f"Beneficiary Name  : {beneficiary_name}")
            print(f"Account Number    : {beneficiary_account_number}")
            print("========================================")

            return True

        except Exception as error:
            connection.rollback()
            print("Failed to add beneficiary:", error)
            return False

        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_beneficiaries(account_id):

        connection = create_connection()

        if connection is None:
            return []

        cursor = connection.cursor(dictionary=True)

        try:
            query = """
            SELECT
                beneficiary_id,
                beneficiary_account_number,
                beneficiary_name,
                created_at
            FROM beneficiaries
            WHERE account_id = %s
            ORDER BY created_at DESC
            """

            cursor.execute(query, (account_id,))

            beneficiaries = cursor.fetchall()

            return beneficiaries

        except Exception as error:
            print("Failed to fetch beneficiaries:", error)
            return []

        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def delete_beneficiary(account_id, beneficiary_id):

        connection = create_connection()

        if connection is None:
            return False

        cursor = connection.cursor()

        try:
            # Check whether the beneficiary belongs to this account
            check_query = """
            SELECT beneficiary_id
            FROM beneficiaries
            WHERE beneficiary_id = %s
            AND account_id = %s
            """

            cursor.execute(
                check_query,
                (beneficiary_id, account_id)
            )

            beneficiary = cursor.fetchone()

            if beneficiary is None:
                print("\nBeneficiary not found.")
                return False

            # Delete beneficiary
            delete_query = """
            DELETE FROM beneficiaries
            WHERE beneficiary_id = %s
            AND account_id = %s
            """

            cursor.execute(
                delete_query,
                (beneficiary_id, account_id)
            )

            connection.commit()

            print("\n========================================")
            print("      BENEFICIARY DELETED SUCCESSFULLY")
            print("========================================")

            return True

        except Exception as error:
            connection.rollback()
            print("Failed to delete beneficiary:", error)
            return False

        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_beneficiary(account_id, beneficiary_id):

        connection = create_connection()

        if connection is None:
            return None

        cursor = connection.cursor(dictionary=True)

        try:
            query = """
            SELECT
                beneficiary_id,
                beneficiary_account_number,
                beneficiary_name
            FROM beneficiaries
            WHERE beneficiary_id = %s
            AND account_id = %s
            """

            cursor.execute(
                query,
                (beneficiary_id, account_id)
            )

            beneficiary = cursor.fetchone()

            return beneficiary

        except Exception as error:
            print("Failed to fetch beneficiary:", error)
            return None

        finally:
            cursor.close()
            connection.close()