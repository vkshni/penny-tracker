# Modules
from pathlib import Path
import csv

BASE_DIR = Path(__file__).parent

# LowLevels

class CSVFile:

    def __init__(self, file_name):
        self.file_path = self.create(file_name)


    def create(self, file_name):

        path = BASE_DIR / file_name
        if not path.exists():
            with open(path, "x") as f:
                pass
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

        expenses = self.csv_handler.read_all()
        if skip_header:
            expenses = expenses[1:]
        return expenses
    
    def add_expense(self, expense_row: list):

        self.csv_handler.append_row(expense_row)
        return True
    
    