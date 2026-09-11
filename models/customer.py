class Customer:

    def _init_(
        self,
        customer_id=None,
        full_name=None,
        phone=None,
        email=None,
        address=None,
        created_at=None
    ):
        self.customer_id = customer_id
        self.full_name = full_name
        self.phone = phone
        self.email = email
        self.address = address
        self.created_at = created_at

    def _str_(self):
        return (
            f"Customer ID: {self.customer_id}\n"
            f"Name: {self.full_name}\n"
            f"Phone: {self.phone}\n"
            f"Email: {self.email}\n"
            f"Address: {self.address}"
        )