from database.connection import create_connection
from models.customer import Customer


class CustomerService:

    @staticmethod
    def create_customer(full_name, phone, email=None, address=None):

        connection = create_connection()

        if connection is None:
            return None

        cursor = connection.cursor()

        query = """
        INSERT INTO customers
        (full_name, phone, email, address)
        VALUES (%s, %s, %s, %s)
        """

        try:
            cursor.execute(
                query,
                (full_name, phone, email, address)
            )

            connection.commit()

            customer_id = cursor.lastrowid

            print("Customer created successfully.")
            print(f"Customer ID: {customer_id}")

            return Customer(
                customer_id=customer_id,
                full_name=full_name,
                phone=phone,
                email=email,
                address=address
            )

        except Exception as error:
            connection.rollback()
            print("Failed to create customer:", error)
            return None

        finally:
            cursor.close()
            connection.close()