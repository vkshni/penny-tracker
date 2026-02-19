# Modules
from datetime import datetime
from entity import Expense
from db import ExpenseDB




class ExpenseTracker:


    def __init__(self):
        self.expensedb = ExpenseDB()

    def add_expense(self, amount, category, date, note=""):
        
        expense_obj = Expense(amount, category, date, note)

        expense_row = expense_obj.to_list()
        self.expensedb.add_expense(expense_row)

        return True
    
    def view_all(self):

        expenses = self.expensedb.get_all_expenses()
        numbered_expenses = [
            [idx+1] + e.to_list()
            for idx, e in enumerate(expenses)]
        return numbered_expenses
    
    def filter_by_category(self, category: str):

        expenses = self.expensedb.get_all_expenses()
        expenses_by_category = [e.to_dict() for e in expenses if e.category == category.lower()]

        return expenses_by_category
    
    @staticmethod
    def parse_date(date_str):

        return datetime.strptime(date_str, "%d-%m-%Y")
    
    def filter_by_date_range(self, start_date, end_date):

        start_date = ExpenseTracker.parse_date(start_date)
        end_date = ExpenseTracker.parse_date(end_date)
        
        expenses = self.expensedb.get_all_expenses()
        expenses_by_date_range = []

        for e in expenses:
            parsed_date = ExpenseTracker.parse_date(e.date)
            if start_date <= parsed_date <= end_date:
                expenses_by_date_range.append(e.to_dict())

        return expenses_by_date_range


    @staticmethod
    def matches_month(date_str, month, year):

        date = datetime.strptime(date_str, "%d-%m-%Y")
        return date.month == month and date.year == year
    
    def monthly_summary(self, month, year):

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

        return {
            "total": total,
            "by_category": by_category
        }
    
    def get_expense_by_display_id(self, display_id):

        expenses = self.expensedb.get_all_expenses()

        if not (1 <= display_id <= len(expenses)):
            return False
        
        expense = expenses[display_id-1]
        return expense
    
    def delete_expense(self, display_id):

        expense = self.get_expense_by_display_id(display_id)

        if not expense:
            return False

        self.expensedb.delete_expense(expense.id)
        return True

    def edit_expense(self, display_id, amount= None, category= None, date= None, note = None):

        expense = self.get_expense_by_display_id(display_id)

        if not expense:
            return False

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
        return True