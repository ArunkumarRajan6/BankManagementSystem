class Account:

    def _init_(
        self,
        account_id=None,
        customer_id=None,
        account_number=None,
        account_type="Savings",
        balance=0,
        pin_hash=None,
        status="Active",
        created_at=None
    ):
        self.account_id = account_id
        self.customer_id = customer_id
        self.account_number = account_number
        self.account_type = account_type
        self.balance = balance
        self.pin_hash = pin_hash
        self.status = status
        self.created_at = created_at

    def _str_(self):
        return (
            f"Account Number: {self.account_number}\n"
            f"Account Type: {self.account_type}\n"
            f"Balance: ₹{self.balance}\n"
            f"Status: {self.status}"
        )