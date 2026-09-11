from getpass import getpass

from services.registration_service import RegistrationService
from services.login_service import LoginService
from services.deposit_service import DepositService
from services.withdraw_service import WithdrawService
from services.transaction_service import TransactionService
from services.transfer_service import TransferService
from services.account_details_service import AccountDetailsService
from services.change_pin_service import ChangePinService
from services.beneficiary_service import BeneficiaryService


from utils.validators import (
    validate_name,
    validate_phone,
    validate_email,
    validate_pin,
    validate_amount
)

def pause_screen():
    input("\nPress Enter to continue...")

def pause_login():
    input("\nPress Enter to continue to your Account Menu...")

def create_account():
    print("\n")
    print("=" * 45)
    print("           CREATE BANK ACCOUNT")
    print("=" * 45)

    # Full name
    while True:
        full_name = input("Enter full name: ")

        valid, result = validate_name(full_name)

        if valid:
            full_name = result
            break

        print(f"Error: {result}")

    # Phone
    while True:
        phone = input("Enter 10-digit phone number: ")

        valid, result = validate_phone(phone)

        if valid:
            phone = result
            break

        print(f"Error: {result}")

    # Email
    while True:
        email = input("Enter email (optional): ")

        valid, result = validate_email(email)

        if valid:
            email = result
            break

        print(f"Error: {result}")

    # Address
    while True:
        address = input("Enter address: ").strip()

        if address:
            break

        print("Error: Address cannot be empty.")

    # Account type
    while True:
        print("\nSelect account type:")
        print("1. Savings")
        print("2. Current")

        account_choice = input("Enter choice (1/2): ").strip()

        if account_choice == "1":
            account_type = "Savings"
            break

        if account_choice == "2":
            account_type = "Current"
            break

        print("Error: Please select 1 or 2.")

    # Initial deposit
    while True:
        initial_deposit = input("Enter initial deposit: ")

        valid, result = validate_amount(initial_deposit)

        if valid:
            initial_deposit = result
            break

        print(f"Error: {result}")

    # PIN
    while True:
        pin = getpass("Enter 4-digit PIN: ")

        valid, result = validate_pin(pin)

        if valid:
            pin = result
            break

        print(f"Error: {result}")

    # Confirm PIN
    while True:
        confirm_pin = getpass("Confirm 4-digit PIN: ")

        if confirm_pin == pin:
            break

        print("Error: PINs do not match.")

    # Register customer and account
    result = RegistrationService.register_customer(
        full_name=full_name,
        phone=phone,
        email=email,
        address=address,
        account_type=account_type,
        initial_deposit=initial_deposit,
        pin=pin
    )

    if result:
        print("\nPlease save your account number securely.")
        print(f"Your Account Number: {result['account_number']}")
        pause_screen()


def login():
    print("\n")
    print("=" * 45)
    print("              ACCOUNT LOGIN")
    print("=" * 45)

    while True:
        account_number = input("Enter account number: ").strip()

        if not account_number:
            print("Error: Account number cannot be empty.")
            continue

        if not account_number.isdigit():
            print("Error: Account number must contain digits only.")
            continue

        if len(account_number) != 10:
            print("Error: Account number must contain exactly 10 digits.")
            continue

        break

    max_attempts = 3
    attempts = 0

    while attempts < max_attempts:

        while True:
            pin = getpass("Enter 4-digit PIN: ")

            valid, result = validate_pin(pin)

            if valid:
                pin = result
                break

            print(f"Error: {result}")

        account = LoginService.login(
            account_number=account_number,
            pin=pin
        )

        if account == "ACCOUNT_NOT_FOUND":
            pause_screen()
            return

        if account:
            pause_login()
            account_menu(account)
            return

        attempts += 1

        if attempts < max_attempts:
            remaining = max_attempts - attempts
            print(f"\nIncorrect PIN. Attempts remaining: {remaining}")
        else:
            print("\nToo many incorrect attempts.")
            print("Login blocked.")
            pause_screen()

def deposit_money(account):
    print("\n")
    print("=" * 45)
    print("              DEPOSIT MONEY")
    print("=" * 45)

    while True:
        amount_input = input("Enter deposit amount: ")

        valid, result = validate_amount(amount_input)

        if valid:
            amount = result
            break

        print(f"Error: {result}")

    success = DepositService.deposit(
        account_id=account["account_id"],
        amount=amount
    )

    if success:
        account["balance"] += amount

    pause_screen()

def withdraw_money(account):
    print("\n")
    print("=" * 45)
    print("             WITHDRAW MONEY")
    print("=" * 45)

    while True:
        amount_input = input("Enter withdrawal amount: ")

        valid, result = validate_amount(amount_input)

        if valid:
            amount = result
            break

        print(f"Error: {result}")

    success = WithdrawService.withdraw(
        account_id=account["account_id"],
        amount=amount
    )

    if success:
        # Update the balance stored in the current session
        account["balance"] -= amount

    pause_screen()

def show_transaction_history(account):
    print("\n")
    print("=" * 70)
    print("                    TRANSACTION HISTORY")
    print("=" * 70)

    transactions = TransactionService.get_transaction_history(
        account_id=account["account_id"]
    )

    if not transactions:
        print("No transactions found.")
        print("=" * 70)
        pause_screen()
        return

    for transaction in transactions:
        print(f"\nTransaction ID : {transaction['transaction_id']}")
        print(f"Date           : {transaction['transaction_date']}")
        print(f"Type           : {transaction['transaction_type']}")
        print(f"Amount         : ₹{transaction['amount']}")
        print(f"Balance After  : ₹{transaction['balance_after']}")
        print(f"Reference No.  : {transaction['reference_number']}")
        print(f"Description    : {transaction['description']}")
        print("-" * 70)

    print("=" * 70)

    pause_screen()

def transfer_money(account):
    print("\n")
    print("=" * 45)
    print("             TRANSFER MONEY")
    print("=" * 45)

    beneficiaries = BeneficiaryService.get_beneficiaries(
        account_id=account["account_id"]
    )

    print("\n1. Transfer to Saved Beneficiary")
    print("2. Transfer to New Account Number")
    print("3. Cancel")
    print("=" * 45)

    choice = input("Enter your choice: ").strip()

    # ----------------------------------------
    # OPTION 1: SAVED BENEFICIARY
    # ----------------------------------------
    if choice == "1":

        if not beneficiaries:
            print("\nNo beneficiaries found.")
            print("Please use option 2 for a direct transfer.")
            pause_screen()
            return

        print("\nYour Beneficiaries:")
        print("-" * 45)

        for beneficiary in beneficiaries:
            print(
                f"{beneficiary['beneficiary_id']}. "
                f"{beneficiary['beneficiary_name']} - "
                f"{beneficiary['beneficiary_account_number']}"
            )

        print("-" * 45)

        while True:
            beneficiary_id_input = input(
                "Enter Beneficiary ID: "
            ).strip()

            if not beneficiary_id_input.isdigit():
                print("Error: Please enter a valid Beneficiary ID.")
                continue

            beneficiary_id = int(beneficiary_id_input)

            beneficiary = BeneficiaryService.get_beneficiary(
                account_id=account["account_id"],
                beneficiary_id=beneficiary_id
            )

            if beneficiary is None:
                print("Error: Beneficiary not found.")
                continue

            receiver_account_number = (
                beneficiary["beneficiary_account_number"]
            )

            print("\n----------------------------------------")
            print(
                f"Beneficiary Name : "
                f"{beneficiary['beneficiary_name']}"
            )
            print(
                f"Account Number   : "
                f"{receiver_account_number}"
            )
            print("----------------------------------------")

            break

    # ----------------------------------------
    # OPTION 2: DIRECT ACCOUNT NUMBER
    # ----------------------------------------
    elif choice == "2":

        receiver_account_number = input(
            "\nEnter receiver account number: "
        ).strip()

        if not receiver_account_number:
            print("Error: Account number cannot be empty.")
            pause_screen()
            return

        if not receiver_account_number.isdigit():
            print("Error: Account number must contain digits only.")
            pause_screen()
            return

        if len(receiver_account_number) != 10:
            print("Error: Account number must contain exactly 10 digits.")
            return

        if receiver_account_number == account["account_number"]:
            print("Error: You cannot transfer money to your own account.")
            pause_screen()
            return

        print("\nReceiver Account Number:")
        print(receiver_account_number)

    # ----------------------------------------
    # OPTION 3: CANCEL
    # ----------------------------------------
    elif choice == "3":

        print("\nTransfer cancelled.")
        pause_screen()
        return

    else:

        print("\nInvalid choice. Please select 1, 2, or 3.")
        pause_screen()
        return

    # ----------------------------------------
    # ENTER TRANSFER AMOUNT
    # ----------------------------------------
    while True:

        amount_input = input(
            "\nEnter transfer amount: "
        )

        valid, result = validate_amount(amount_input)

        if valid:
            amount = result
            break

        print(f"Error: {result}")

    # ----------------------------------------
    # CONFIRM TRANSFER
    # ----------------------------------------
    confirmation = input(
        "\nConfirm transfer? (yes/no): "
    ).strip().lower()

    if confirmation != "yes":
        print("\nTransfer cancelled.")
        return

    # ----------------------------------------
    # PERFORM TRANSFER
    # ----------------------------------------
    success = TransferService.transfer(
        sender_account_id=account["account_id"],
        receiver_account_number=receiver_account_number,
        amount=amount
    )

    if success:
        account["balance"] -= amount

    pause_screen()

def show_account_details(account):
    print("\n")
    print("=" * 55)
    print("                 ACCOUNT DETAILS")
    print("=" * 55)

    details = AccountDetailsService.get_account_details(
        account_id=account["account_id"]
    )

    if details is None:
        print("Unable to fetch account details.")
        print("=" * 55)
        pause_screen()
        return

    print("\nCUSTOMER INFORMATION")
    print("-" * 55)
    print(f"Customer ID     : {details['customer_id']}")
    print(f"Full Name       : {details['full_name']}")
    print(f"Phone           : {details['phone']}")
    print(f"Email           : {details['email'] or 'Not provided'}")
    print(f"Address         : {details['address']}")

    print("\nACCOUNT INFORMATION")
    print("-" * 55)
    print(f"Account Number  : {details['account_number']}")
    print(f"Account Type    : {details['account_type']}")
    print(f"Balance         : ₹{details['balance']}")
    print(f"Status          : {details['status']}")
    print(f"Created At      : {details['account_created_at']}")

    print("=" * 55)

    pause_screen()

def change_pin(account):
    print("\n")
    print("=" * 45)
    print("              CHANGE PIN")
    print("=" * 45)

    current_pin = getpass("Enter current PIN: ")

    valid, result = validate_pin(current_pin)

    if not valid:
        print(f"Error: {result}")
        return

    while True:
        new_pin = getpass("Enter new PIN: ")

        valid, result = validate_pin(new_pin)

        if not valid:
            print(f"Error: {result}")
            continue

        confirm_pin = getpass("Confirm new PIN: ")

        if new_pin != confirm_pin:
            print("Error: New PINs do not match.")
            continue

        if new_pin == current_pin:
            print("Error: New PIN must be different from current PIN.")
            continue

        break

    success = ChangePinService.change_pin(
        account_id=account["account_id"],
        current_pin=current_pin,
        new_pin=new_pin
    )

    if success:
        print("You can continue using your account.")

    pause_screen()

def add_beneficiary(account):
    print("\n")
    print("=" * 45)
    print("             ADD BENEFICIARY")
    print("=" * 45)

    while True:
        beneficiary_account_number = input("Enter beneficiary account number: ").strip()

        if not beneficiary_account_number:
            print("Error: Account number cannot be empty.")
            continue

        if not beneficiary_account_number.isdigit():
            print("Error: Account number must contain digits only.")
            continue

        if len(beneficiary_account_number) != 10:
            print("Error: Account number must contain exactly 10 digits.")
            continue

        if beneficiary_account_number == account["account_number"]:
            print("Error: You cannot add your own account as a beneficiary.")
            continue

        break

    while True:
        beneficiary_name = input("Enter beneficiary name: ").strip()

        valid, result = validate_name(beneficiary_name)

        if valid:
            beneficiary_name = result
            break

        print(f"Error: {result}")

    success = BeneficiaryService.add_beneficiary(
        account_id=account["account_id"],
        beneficiary_account_number=beneficiary_account_number,
        beneficiary_name=beneficiary_name
    )

    if success:
        print("\nBeneficiary is ready for future transfers.")

    pause_screen()

def view_beneficiaries(account):
    print("\n")
    print("=" * 70)
    print("                    MY BENEFICIARIES")
    print("=" * 70)

    beneficiaries = BeneficiaryService.get_beneficiaries(
        account_id=account["account_id"]
    )

    if not beneficiaries:
        print("No beneficiaries found.")
        print("=" * 70)
        pause_screen()
        return

    for beneficiary in beneficiaries:
        print(f"\nBeneficiary ID   : {beneficiary['beneficiary_id']}")
        print(f"Name             : {beneficiary['beneficiary_name']}")
        print(
            f"Account Number   : "
            f"{beneficiary['beneficiary_account_number']}"
        )
        print(f"Added On         : {beneficiary['created_at']}")
        print("-" * 70)

    print("=" * 70)

    pause_screen()

def delete_beneficiary(account):
    print("\n")
    print("=" * 45)
    print("            DELETE BENEFICIARY")
    print("=" * 45)

    beneficiaries = BeneficiaryService.get_beneficiaries(
        account_id=account["account_id"]
    )

    if not beneficiaries:
        print("No beneficiaries found.")
        pause_screen()
        return

    print("\nYour Beneficiaries:")

    for beneficiary in beneficiaries:
        print(
            f"{beneficiary['beneficiary_id']}. "
            f"{beneficiary['beneficiary_name']} - "
            f"{beneficiary['beneficiary_account_number']}"
        )

    while True:
        beneficiary_id_input = input(
            "\nEnter Beneficiary ID to delete: "
        ).strip()

        if not beneficiary_id_input.isdigit():
            print("Error: Please enter a valid Beneficiary ID.")
            continue

        beneficiary_id = int(beneficiary_id_input)
        break

    confirmation = input(
        "Are you sure you want to delete this beneficiary? (yes/no): "
    ).strip().lower()

    if confirmation != "yes":
        print("\nDeletion cancelled.")
        return

    success = BeneficiaryService.delete_beneficiary(
        account_id=account["account_id"],
        beneficiary_id=beneficiary_id
    )

    if success:
        print("Beneficiary removed from your account.")

    pause_screen()

def account_menu(account):
    while True:
        print("\n")
        print("=" * 45)
        print("             ACCOUNT MENU")
        print("=" * 45)
        print(f"Account Number : {account['account_number']}")
        print(f"Account Type   : {account['account_type']}")
        print("=" * 45)
        print("1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transfer")
        print("5. Transaction History")
        print("6. Account Details")
        print("7. Change PIN")
        print("8. Add Beneficiary")
        print("9. View Beneficiary")
        print("10. Delete Beneficiary")
        print("11. Logout")
        print("=" * 45)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            print(f"\nCurrent Balance: ₹{account['balance']}")
            pause_screen()

        elif choice == "2":
            deposit_money(account)

        elif choice == "3":
            withdraw_money(account)

        elif choice == "4":
            transfer_money(account)

        elif choice == "5":
            show_transaction_history(account)

        elif choice == "6":
            show_account_details(account)

        elif choice == "7":
            change_pin(account)

        elif choice == "8":
            add_beneficiary(account)

        elif choice == "9":
            view_beneficiaries(account)

        elif choice == "10":
            delete_beneficiary(account)

        elif choice == "11":
            print("\nLogged out successfully.")
            break

        else:
            print("\nInvalid choice. Please select 1 to 11.")
            pause_screen()


def main():
    while True:
        print("\n")
        print("=" * 45)
        print("        BANK MANAGEMENT SYSTEM")
        print("=" * 45)
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")
        print("=" * 45)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            create_account()

        elif choice == "2":
            login()

        elif choice == "3":
            print("\nThank you for using our Bank Management System.")
            break

        else:
            print("\nInvalid choice. Please select 1, 2, or 3.")


if __name__ == "__main__":
    main()