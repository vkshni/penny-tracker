"""
Database Module

Handles all CSV file operations and data persistence for Penny Tracker.
Provides low-level CSV operations and high-level expense database management.
"""

# Modules
from pathlib import Path
import csv
from entity import Expense
from exceptions import *

BASE_DIR = Path(__file__).parent

# LowLevels

class CSVFile:
    """
    Low-level CSV file handler.
    
    Manages CSV file creation, reading, and writing operations.
    
    Attributes:
        file_path (Path): Path to the CSV file
    """


    def __init__(self, file_name: str) -> None:
        """
        Initialize CSV file handler.
        
        Args:
            file_name (str): Name of the CSV file
        """

        self.file_path = self.create(file_name)

    def create(self, file_name: str) -> str:
        """
        Create CSV file with header if it doesn't exist.
        
        Args:
            file_name (str): Name of the CSV file
        
        Returns:
            Path: Path object to the CSV file
        """

        path = BASE_DIR / file_name
        if not path.exists():
            with open(path, "x") as f:
                writer = csv.writer(f)
                writer.writerow(["id","amount","category","date","note"])
        return path
    
    def read_all(self):
        """
        Read all rows from CSV file.
        
        Returns:
            list: List of rows (each row is a list of strings)
        """

        with open(self.file_path, "r") as f:

            reader = csv.reader(f)
            rows = [row for row in reader]
            return rows
        
    def write_all(self, rows: list[list]) -> None:
        """
        Write all rows to CSV file (overwrites existing content).
        
        Args:
            rows (list): List of rows to write (including header)
        """

        with open(self.file_path, "w", newline = "" ) as f:

            writer = csv.writer(f)
            writer.writerows(rows)

    def append_row(self, row: list) -> None:
        """
        Append a single row to CSV file.
        
        Args:
            row (list): Row data to append
        """

        with open(self.file_path, "a", newline="") as f:

            writer = csv.writer(f)
            writer.writerow(row)
        

class ExpenseDB:
    """
    High-level expense database manager.
    
    Provides CRUD operations for expenses stored in CSV format.
    
    Attributes:
        csv_handler (CSVFile): CSV file handler instance
    """


    def __init__(self) -> None:
        """Initialize expense database with expenses.csv file."""

        self.csv_handler = CSVFile("expenses.csv")

    def get_all_expenses(self, skip_header = True) -> list[Expense]:
        """
        Retrieve all expenses from database.
        
        Args:
            skip_header (bool): Whether to skip the header row (default: True)
        
        Returns:
            list[Expense]: List of Expense objects
        """

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
    
    def add_expense(self, expense_row: list) -> bool:
        """
        Add new expense to database.
        
        Args:
            expense_row (list): Expense data as list [id, amount, category, date, note]
        
        Returns:
            bool: True if successful
        """

        self.csv_handler.append_row(expense_row)
        return True

    def delete_expense(self, expense_id: str) -> bool:
        """
        Delete expense by UUID.
        
        Args:
            expense_id (str): UUID of expense to delete
        
        Returns:
            bool: True if deleted
        
        Raises:
            ExpenseNotFoundError: if expense object not found
        """

        rows = self.csv_handler.read_all()

        filtered = [r for r in rows if r[0] != expense_id]

        if len(rows) == len(filtered):
            raise ExpenseNotFoundError("Expense doesn't exist: not found")
        
        self.csv_handler.write_all(filtered)
        return True
    
    def update_expense(self, expense: Expense) -> bool:
        """
        Update existing expense by UUID.
        
        Args:
            expense (Expense): Updated expense object
        
        Returns:
            bool: True if updated
        
        Raises:
            ExpenseNotFoundError: if expense object not found
        """

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
        
        self.csv_handler.write_all([header]+data_rows)
        return True



    
    