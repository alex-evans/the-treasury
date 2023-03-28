
import csv
from datetime import datetime
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Transactions
from models import TxnNames


load_dotenv()

USERNAME = os.environ.get('USERNAME')
PASSWORD = os.environ.get('PASSWORD')
DATABASE = os.environ.get('DATABASE')
engine = create_engine(
    f'postgresql://{USERNAME}:{PASSWORD}@localhost/{DATABASE}'
)
Session = sessionmaker(bind=engine)


#######################
# US BANK
#######################

def usbank_process_txn_name(full_txn_name):
    if 'WEB AUTHORIZED PMT ' in full_txn_name:
        return full_txn_name.removeprefix('WEB AUTHORIZED PMT ')

    if 'ELECTRONIC WITHDRAWAL ' in full_txn_name:
        return full_txn_name.removeprefix('ELECTRONIC WITHDRAWAL ')

    if 'DEBIT PURCHASE -VISA ' in full_txn_name:
        return full_txn_name.removeprefix('DEBIT PURCHASE -VISA ')

    if 'ELECTRONIC DEPOSIT ' in full_txn_name:
        return full_txn_name.removeprefix('ELECTRONIC DEPOSIT ')

    if 'Netflix' in full_txn_name:
        return 'Netflix'

    return full_txn_name


def load_usbank_txns(session, csv_reader, filename):
    
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
            continue
        
        full_name = row['Name']
        slim_name = usbank_process_txn_name(full_name)

        if 'MONTHLY MAINTENANCE FEE' in slim_name:
            continue

        if 'REVERSED ATM FEE' in slim_name:
            continue

        if 'MONTHLY MAINTENANCE FEE WAIVED' in slim_name:
            continue

        if 'AMEX EPAYMENT' in slim_name:
            # skip amex payments as captured by amex files
            continue

        db_txn_name = session.query(TxnNames).filter(TxnNames.name == slim_name).first()
        if not db_txn_name:
            raise ValueError('Txn Name not found in db:', slim_name)
        
        revenue = True
        if '-' in row['Amount']:
            revenue = False

        date_list = row['Date'].split('-')
        date = datetime(int(date_list[0]), int(date_list[1]), int(date_list[2]))

        txn = Transactions(
            filename = filename,
            date = date,
            amount=abs(float(row['Amount'])),
            revenue=revenue,
            source='us bank',
            name=db_txn_name
        )

        session.add(txn)


#######################
# AMERICAN EXPRESS
#######################

def amex_process_txn_name(full_txn_name):
    if 'AMAZON' in full_txn_name:
        return 'AMAZON'
    
    if 'STARBUCKS' in full_txn_name:
        return 'STARBUCKS'
    
    if 'T-MOBILE' in full_txn_name:
        return 'T-MOBILE'
    
    if 'YOUTUBE TV' in full_txn_name:
        return 'YOUTUBE TV'
    
    if 'PRIME VIDEO' in full_txn_name:
        return 'PRIME VIDEO'
    
    if 'HOMEDEPOT' in full_txn_name or 'THE HOME DEPOT' in full_txn_name:
        return 'HOMEDEPOT'
    
    if 'DISNEYPLUS' in full_txn_name:
        return 'DISNEYPLUS'
    
    return full_txn_name


def load_amex_txns(session, csv_reader, filename):
    
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
            continue

        if 'MOBILE PAYMENT' in row['Description']:
            continue

        name = amex_process_txn_name(row['Description'])

        db_txn_name = session.query(TxnNames).filter(TxnNames.name == name).first()
        if not db_txn_name:
            raise ValueError('Transaction Name not found in db:', name)

        revenue = True
        if '-' in row['Amount']:
            revenue = False

        date_list = row['Date'].split('/')
        date = datetime(int(date_list[2]), int(date_list[0]), int(date_list[1]))

        txn = Transactions(
            filename = filename,
            date = date,
            amount=abs(float(row['Amount'])),
            revenue=revenue,
            source='amex',
            name=db_txn_name
        )

        session.add(txn)


#######################
#######################

def save_file(filename):
    print('Saving Txns for:', filename)

    session = Session()

    try:

        with open(f'raw_data/{filename}', mode='r') as bank_csv:
            csv_reader = csv.DictReader(bank_csv)

            if filename.startswith('usbank'):
                load_usbank_txns(session, csv_reader, filename)

            elif filename.startswith('amex'):
                load_amex_txns(session, csv_reader, filename)

            else:
                ValueError('Bank type not found for file')

        session.commit()

    except Exception as e:
        print('Failed to save txn:', e)
        session.rollback()

    print('Done Saving')