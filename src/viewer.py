
import calendar
from datetime import datetime
from dotenv import load_dotenv
import os
from rich.console import Console
from rich.table import Table
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Transactions


load_dotenv()

USERNAME = os.environ.get('USERNAME')
PASSWORD = os.environ.get('PASSWORD')
DATABASE = os.environ.get('DATABASE')
engine = create_engine(
    f'postgresql://{USERNAME}:{PASSWORD}@localhost/{DATABASE}'
)
Session = sessionmaker(bind=engine)


def month_view(year, month):
    session = Session()

    (_, end_day) = calendar.monthrange(year, month)
    
    start_date = datetime(year, month, 1)
    end_date = datetime(year, month, end_day)
    
    months_transactions = session.query(Transactions).filter(Transactions.date.between(start_date, end_date)).all()

    table = Table(title=f'Month View Debits: {start_date} - {end_date}')
    table.add_column('Date')
    table.add_column('Group')
    table.add_column('Sub-Group')
    table.add_column('Name')
    table.add_column('Amount')

    month_total = 0.00
    for txn in months_transactions:
        if txn.revenue:
            amount = txn.amount
        else:
            amount = -abs(txn.amount)
        
        table.add_row(str(txn.date), txn.name.group, txn.name.sub_group, txn.name.name, str(amount))
        month_total =+ amount 
        
    console = Console()
    console.print(table)

    print('Month:', month_total)
