

class Expense:

    def __init__(self, id, amount, category, date, note = ""):
        self.id = id
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
    
    def from_dict(self, expense_dict):

        id = expense_dict[id]
        amount = expense_dict[amount]
        category = expense_dict[category]
        date= expense_dict[date]
        note = expense_dict[note]

        obj = Expense(id, amount, category, date, note)
        return obj


    def validate_fields(self):

        if not self.id :
            raise ValueError("Empty Field")
        
        if not self.amount or self.amount <=0:
            raise ValueError("Amount should be greater than 0")
        
        if not self.category or not self.category.isalpha():
            raise ValueError("Category name should be a single string")

        # if not self.date or not self.date.isalpha():
        #     raise ValueError("Data should be in format DD-MM-YYYY")