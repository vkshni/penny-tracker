# 💰 Penny Tracker

A simple, lightweight command-line expense tracker built in Python. Track your expenses with ease using file-based storage (CSV).

## ✨ Features

- ➕ **Add expenses** with amount, category, date, and notes
- 📋 **View all expenses** with display IDs for easy reference
- 🔍 **Filter expenses** by category or date range
- 📊 **Monthly summaries** with category-wise breakdown
- ✏️ **Edit expenses** by display ID
- 🗑️ **Delete expenses** with confirmation prompt
- 💾 **CSV storage** - simple, portable, human-readable

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher

### Setup

1. Clone or download this repository
2. Navigate to the project directory:
```bash
   cd penny-tracker
```

3. **Windows CMD Setup:**
   - Create `penny.bat` in the project folder (already included)
   - Add project folder to your PATH, or run from project directory

4. Verify installation:
```cmd
   penny --help
```

## 📖 Usage

### Add an Expense
```cmd
penny add --amount 50 --category food --date 20-02-2026 --note "lunch at cafe"
```

### View All Expenses
```cmd
penny view
```

Output:
```
#    Amount     Category        Date          Note
-----------------------------------------------------------------
1    50.00      food            20-02-2026    lunch at cafe
2    120.00     transport       19-02-2026    uber ride
3    30.00      food            18-02-2026    breakfast
```

### Filter by Category
```cmd
penny filter --category food
```

### Filter by Date Range
```cmd
penny filter --from 01-02-2026 --to 28-02-2026
```

### Monthly Summary
```cmd
penny summary --month 2 --year 2026
```

Output:
```
Monthly Summary for 02/2026

Total Spent: ₹200.00

Category Breakdown:
----------------------------------------
food                 ₹80.00
transport            ₹120.00
```

### Edit an Expense
```cmd
penny edit 1 --amount 75 --note "expensive lunch"
```

### Delete an Expense
```cmd
penny delete 2
```

You'll be prompted for confirmation before deletion.

## 📁 Project Structure
```
penny-tracker/
├── penny.py           # CLI interface
├── tracker.py         # Core business logic
├── entity.py          # Expense entity and validation
├── db.py              # CSV database operations
├── exceptions.py      # Custom exception classes
├── expenses.csv       # Data storage (created automatically)
├── penny.bat          # Windows batch file
└── README.md          # Documentation
```

## 🎯 Data Format

### Date Format
Always use `DD-MM-YYYY` format (e.g., `20-02-2026`)

### Categories
- Free-text, lowercase preferred
- Examples: `food`, `transport`, `shopping`, `bills`, `entertainment`

### Amount
- Positive numbers only
- Automatically converted to float

## 🛠️ Technical Details

- **Language:** Python 3.8+
- **Storage:** CSV (Comma-Separated Values)
- **ID System:** UUID4 for internal tracking, display IDs (1,2,3...) for user interaction
- **Architecture:** Layered (CLI → Business Logic → Data Access → Storage)

## 🐛 Error Handling

Penny Tracker provides helpful error messages:
```cmd
penny add --amount -50 --category food --date 20-02-2026
✗ Invalid Amount: Amount must be greater than 0, got: -50.0
```
```cmd
penny add --amount 50 --category food --date 2026-02-20
✗ Invalid Date: Invalid date format: '2026-02-20'
Expected format: DD-MM-YYYY (e.g., 15-02-2026)
```

## 📝 Examples

### Track Daily Expenses
```cmd
penny add --amount 45 --category food --date 21-02-2026 --note "breakfast"
penny add --amount 120 --category transport --date 21-02-2026 --note "cab to office"
penny add --amount 200 --category shopping --date 21-02-2026 --note "groceries"
```

### Review Monthly Spending
```cmd
penny summary --month 2 --year 2026
```

### Find Specific Expenses
```cmd
rem All food expenses
penny filter --category food

rem This week's expenses
penny filter --from 15-02-2026 --to 21-02-2026
```

## 🤝 Contributing

This is a Week 2 micro-system project. Feel free to fork and enhance!

## 📄 License

Free to use and modify.

**Made with ☕ by Vijay Kumar Sahani**