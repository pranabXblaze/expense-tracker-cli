import argparse
import csv
import os
from datetime import datetime

DATA_FILE = 'expenses.csv'
#Loading existing data
def load_data():
    expenses = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                row['amount'] = float(row['amount'])
                row['id'] = int(row['id'])
                expenses.append(row)
    return expenses


#save  update expenses
def save_data(data):
    with open(DATA_FILE, 'w') as file:
        fieldnames = ['id', 'date' , 'description', 'amount']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for expense in data:
            writer.writerow(expense)


#add new expense
def add_expense(description, amount):
    expenses = load_data()
    new_id = len(expenses) +1
    expense = {
        'id' : new_id,
        'date' : str(datetime.now().date()),
        'description' : description,
        'amount': amount
    }
    expenses.append(expense)
    save_data(expenses)
    print(f'Expense added suceessfully with ID: {new_id}')

#list all the expense
def list_expenses():
    expenses = load_data()
    print(f"{'ID':<5} {'Date':<12} {'Description':<15} {'Amount':<10}")
    for expense in expenses:
        print(f"{expense['id']:<5} {expense['date']:<12} {expense['description']:<15} ${expense['amount']:<10}")



#delete a expense 

def delete_expense(expense_id):
    expenses = load_data()
    updated_expenses = [e for e in expenses if e['id'] != expense_id]

    if len(updated_expenses) != len(expenses):
       save_data(updated_expenses)
       print(f'Expense (ID {expense_id}) deleted successfully.')
    else:
        print('Expense ID not found.')

#Show summary and the sum amount

def show_summary(month= None):
    expenses = load_data()
    total = 0
    for expense in expenses:
        if month:
            if datetime.strptime(expense['date'], '%Y-%m-%d').month == month :
                total += expense['amount']
        else :
            total += expense['amount']
    if month :
        print(f'Total expense for Month :{month} : ${total}')
    else :
        print(f'Total expenses: {total}')

def main():
    parser = argparse.ArgumentParser(description="Expense Tracker CLI")
    
    subparsers = parser.add_subparsers(dest='command', help='Subcommands')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new expense')
    add_parser.add_argument('--description', required=True, help='Description of the expense')
    add_parser.add_argument('--amount', required=True, type=float, help='Amount of the expense')

    # List command
    list_parser = subparsers.add_parser('list', help='List all expenses')

    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete an expense')
    delete_parser.add_argument('--id', required=True, type=int, help='ID of the expense to delete')

    # Summary command
    summary_parser = subparsers.add_parser('summary', help='Show total expenses')
    summary_parser.add_argument('--month', type=int, help='Month to filter expenses')

    # Parse the arguments  
    args = parser.parse_args()

    # Handle the commands
    if args.command == 'add':
        add_expense(args.description, args.amount)
    elif args.command == 'list':
        list_expenses()
    elif args.command == 'delete':
        delete_expense(args.id)
    elif args.command == 'summary':
        show_summary(args.month)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
    
