# Modules
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
        return expenses