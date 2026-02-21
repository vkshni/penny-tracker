# Modules
from pathlib import Path
import csv
from entity import Expense
from exceptions import *

BASE_DIR = Path(__file__).parent

# LowLevels

class CSVFile:

    def __init__(self, file_name):
        self.file_path = self.create(file_name)


    def create(self, file_name):

        path = BASE_DIR / file_name
        if not path.exists():
            with open(path, "x") as f:
                writer = csv.writer(f)
                writer.writerow(["id","amount","category","date","note"])
        return path
    
    def read_all(self):

        with open(self.file_path, "r") as f:

            reader = csv.reader(f)
            rows = [row for row in reader]
            return rows
        
    def write_all(self, rows):

        with open(self.file_path, "w", newline = "" ) as f:

            writer = csv.writer(f)
            writer.writerows(rows)

    def append_row(self, row):

        with open(self.file_path, "a", newline="") as f:

            writer = csv.writer(f)
            writer.writerow(row)
        

class ExpenseDB:

    def __init__(self):
        self.csv_handler = CSVFile("expenses.csv")

    def get_all_expenses(self, skip_header = True):

        rows = self.csv_handler.read_all()
        if skip_header:
            rows = rows[1:]
        
        expenses = [Expense.from_dict({
            "id": r[0],
            "amount": r[1],
            "category": r[2],
            "date": r[3],
            "note": r[4]
        }) for r in rows if r and len(r) == 5]
        return expenses
    
    def add_expense(self, expense_row: list):

        self.csv_handler.append_row(expense_row)
        return True

    def delete_expense(self, expense_id: str):

        rows = self.csv_handler.read_all()

        filtered = [r for r in rows if r[0] != expense_id]

        if len(rows) == len(filtered):
            raise ExpenseNotFoundError("Expense doesn't exist: not found")
            return False
        
        self.csv_handler.write_all(filtered)
        return True
    
    def update_expense(self, expense: Expense):

        rows = self.csv_handler.read_all()
        header = rows[0]
        data_rows = rows[1:]

        updated = False

        for i, r in enumerate(data_rows):
            if r[0] == expense.id:
                data_rows[i] = expense.to_list()
                updated = True
                break

        if not updated:
            raise ExpenseNotFoundError("Expense doesn't exist: not found")
            return False
        
        self.csv_handler.write_all([header]+data_rows)
        return True



    
    