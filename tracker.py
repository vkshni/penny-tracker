# Modules
from datetime import datetime
from entity import Expense
from db import ExpenseDB
from exceptions import *
from logger import setup_logger




class ExpenseTracker:


    def __init__(self):
        self.expensedb = ExpenseDB()
        self.logger = setup_logger()

    def add_expense(self, amount, category, date, note=""):
        

        expense_obj = Expense(amount, category, date, note)

        expense_row = expense_obj.to_list()
        self.expensedb.add_expense(expense_row)

        msg = f"Added Expense with amount '{amount}' category '{category}' date '{date}' and note '{note}'"
        self.logger.info(msg)

        return True
    
    def view_all(self):

        expenses = self.expensedb.get_all_expenses()
        if not expenses:
            msg = f"Expense data not found"
            self.logger.warning(msg)
            return
        
        numbered_expenses = [
            [idx+1] + e.to_list()
            for idx, e in enumerate(expenses)]
        
        msg = f"View expense data"
        self.logger.info(msg)

        return numbered_expenses
    
    def filter_by_category(self, category: str):

        expenses = self.expensedb.get_all_expenses()
        expenses_by_category = [e.to_dict() for e in expenses if e.category == category.lower()]

        if not expenses_by_category:
            msg = f"Category '{category}' not found"
            self.logger.warning(msg)
            return 

        msg = f"Filtered by category '{category}'"
        self.logger.info(msg)

        return expenses_by_category
    
    def parse_date(self, date_str):
        try:
            return datetime.strptime(date_str, "%d-%m-%Y")
        except:
            msg = f"Invalid date provided in parser, '{date_str}'"
            self.logger.error(msg)
            raise InvalidDateError(
                f"Invalid date format: '{date_str}'\n"
                f"Expected format: DD-MM-YYYY (e.g., 15-02-2026)"
            )
        
    def filter_by_date_range(self, start_date, end_date):

        start_date = self.parse_date(start_date)
        end_date = self.parse_date(end_date)
        
        expenses = self.expensedb.get_all_expenses()
        expenses_by_date_range = []

        for e in expenses:
            parsed_date = self.parse_date(e.date)
            if start_date <= parsed_date <= end_date:
                expenses_by_date_range.append(e.to_dict())

        if not expenses_by_date_range:
            msg = f"No data between '{start_date}' and '{end_date}'"
            self.logger.warning(msg)
            return

        msg = f"Filtered data by date range '{start_date}' and '{end_date}'"
        self.logger.info(msg)
        return expenses_by_date_range


    @staticmethod
    def matches_month(date_str, month, year):

        date = datetime.strptime(date_str, "%d-%m-%Y")
        return date.month == month and date.year == year
        
    def monthly_summary(self, month, year):

        if not (1<=month<=12):
            msg = f"Invalid month provided, '{month}'"
            self.logger.error(msg)
            raise InvalidDateError(f"Month must be between 1-12, got: {month}")
        
        if not (2000<=year<=2100):
            msg = f"Invalid year provided, '{year}'"
            self.logger.error(msg)
            raise InvalidDateError(f"Year seems invalid: {year}")

        expenses = self.expensedb.get_all_expenses()

        monthly_expenses = [
            e
            for e in expenses
            if ExpenseTracker.matches_month(e.date, month, year)
        ]

        total = sum(e.amount for e in monthly_expenses)

        by_category = {}

        for e in monthly_expenses:
            by_category[e.category] = by_category.get(e.category, 0) + e.amount


        msg = f"Monthly summary for month '{month}' and year '{year}'"
        self.logger.info(msg)

        return {
            "total": total,
            "by_category": by_category
        }
    
    def get_expense_by_display_id(self, display_id):

        expenses = self.expensedb.get_all_expenses()

        if not (1 <= display_id <= len(expenses)):
            msg = f"Expense with display id '{display_id}' not found"
            self.logger.warning(msg)
            raise ExpenseNotFoundError(f"Display ID {display_id} not found")

        
        expense = expenses[display_id-1]

        msg = f"Display ID '{display_id}' choosen"
        self.logger.info(msg)
        return expense
    
    def delete_expense(self, display_id):

        expense = self.get_expense_by_display_id(display_id)

        if not expense:
            msg = f"Expense with display id '{display_id}' not found"
            self.logger.warning(msg)
            raise ExpenseNotFoundError(f"Display ID {display_id} not found")

        self.expensedb.delete_expense(expense.id)

        msg = f"Expense with display ID '{display_id}' deleted"
        self.logger.info(msg)

        return True

    def edit_expense(self, display_id, amount= None, category= None, date= None, note = None):

        expense = self.get_expense_by_display_id(display_id)

        if not expense:
            msg = f"Expense with display id '{display_id}' not found"
            self.logger.warning(msg)

            raise ExpenseNotFoundError(f"Display ID {display_id} not found")

        if amount is not None:
            expense.amount = float(amount)
        if category is not None:
            expense.category = category.lower()
        if date is not None:
            expense.date = date
        if note is not None:
            expense.note = note

        expense.validate_fields()

        self.expensedb.update_expense(expense)

        msg = f"Expense with display id '{display_id}' edited"
        self.logger.info(msg)

        return True