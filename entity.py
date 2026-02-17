from datetime import datetime
from uuid import uuid4

class Expense:

    def __init__(self, amount, category, date, note = "", id=None):
        self.id = str(id) if id else str(uuid4())
        self.amount = float(amount)
        self.category = category.lower()
        self.date = date
        self.note = note

        self.validate_fields()

    def to_dict(self):
        
        expense_dict = {
            "id": self.id,
            "amount": self.amount,
            "category": self.category,
            "date": self.date,
            "note": self.note
        }

        return expense_dict
    
    def to_list(self):

        expense_row = [
            self.id,
            self.amount,
            self.category,
            self.date,
            self.note
        ]

        return expense_row
    
    @classmethod
    def from_dict(cls, expense_dict):

        return cls(
            expense_dict["id"],
            expense_dict["amount"],
            expense_dict["category"],
            expense_dict["date"],
            expense_dict["note"]
        )
        


    def validate_fields(self):

        if not self.id :
            raise ValueError("Empty Field")
        
        if self.amount <=0:
            raise ValueError("Amount should be greater than 0")
        
        if not self.category.strip():
            raise ValueError("Category cannot be empty")

        try:
            datetime.strptime(self.date, "%d-%m-%Y")
        except ValueError:
            raise ValueError(f"Date must be in DD-MM-YYYY format, got: {self.date}")