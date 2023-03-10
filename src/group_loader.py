
import csv
import json


def usbank_process_txn_name(full_txn_name):
    if 'WEB AUTHORIZED PMT ' in full_txn_name:
        return full_txn_name.removeprefix('WEB AUTHORIZED PMT ')

    if 'ELECTRONIC WITHDRAWAL ' in full_txn_name:
        return full_txn_name.removeprefix('ELECTRONIC WITHDRAWAL ')

    if 'DEBIT PURCHASE -VISA ' in full_txn_name:
        return full_txn_name.removeprefix('DEBIT PURCHASE -VISA ')

    if 'ELECTRONIC DEPOSIT ' in full_txn_name:
        return full_txn_name.removeprefix('ELECTRONIC DEPOSIT ')

    return full_txn_name


def load_usbank(csv_reader):
    bank_data = []
    line_count = 0
    
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
            continue

        full_name = row['Name']
        slim_name = usbank_process_txn_name(full_name)

        slim_name = row['Name']

        bank_data.append(
            {
                'type': row['Transaction'],
                'name': row['Name']
            }
        )

    return bank_data


def load_amex(csv_reader):
    bank_data = []
    line_count = 0

    for row in csv_reader:
        if line_count == 0:
            line_count += 1
            continue

        if 'MOBILE PAYMENT' in row['Description']:
            continue

        bank_data.append(
            {
                'type': 'DEBIT',
                'name': row['Description']
            }
        )

    return bank_data


def process_bank_and_groups(group_dict, bank_data):



def load(filename):
    with open('../group_dict.json') as group_file:
        group_dict = json.load(group_file)

    with open(f'../raw_data/{filename}', mode='r') as bank_csv:
        csv_reader = csv.DictReader(bank_csv)

        if filename.startswith('usbank'):
            bank_data = load_usbank(csv_reader)

        elif filename.startswith('amex'):
            bank_data = load_amex(csv_reader)

        else:
            ValueError('Bank type not found for file')
        
        process_bank_and_groups(group_dict, bank_data)
