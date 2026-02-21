from datetime import datetime
from uuid import uuid4

from exceptions import *
from logger import setup_logger

logger = setup_logger()

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
            amount = expense_dict["amount"],
            category = expense_dict["category"],
            date = expense_dict["date"],
            note = expense_dict["note"],
            id = expense_dict["id"]
        )
        


    def validate_fields(self):

        if not self.id :
            msg = f"Empty expense ID"
            logger.error(msg)
            raise EmptyFieldError("Empty Field")
        
        if self.amount <=0:
            msg = f"Invalid amount '{self.amount}'"
            logger.error(msg)
            raise InvalidAmountError("Amount should be greater than 0")
        
        if not self.category.strip():
            msg = f"Empty expense ID"
            logger.error(msg)
            raise EmptyFieldError("Category cannot be empty")

        try:
            datetime.strptime(self.date, "%d-%m-%Y")
        except ValueError:
            msg = f"Invalid date format, {self.date}"
            logger.error(msg)
            raise InvalidDateError(f"Date must be in DD-MM-YYYY format, got: {self.date}")