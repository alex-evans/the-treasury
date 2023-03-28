
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

    if 'Netflix' in full_txn_name:
        return 'Netflix'

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

        if 'MONTHLY MAINTENANCE FEE' in slim_name:
            continue

        if 'REVERSED ATM FEE' in slim_name:
            continue

        if 'MONTHLY MAINTENANCE FEE WAIVED' in slim_name:
            continue

        if 'AMEX EPAYMENT' in slim_name:
            # skip amex payments as captured by amex files
            continue

        bank_data.append(
            {
                'type': row['Transaction'],
                'name': slim_name
            }
        )

    return bank_data


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


def load_amex(csv_reader):
    bank_data = []
    line_count = 0

    for row in csv_reader:
        if line_count == 0:
            line_count += 1
            continue

        if 'MOBILE PAYMENT' in row['Description']:
            continue

        name = amex_process_txn_name(row['Description'])

        if '-' in row['Amount']:
            txn_type = 'CREDIT'
        else:
            txn_type = 'DEBIT'

        bank_data.append(
            {
                'type': txn_type,
                'name': name
            }
        )

    return bank_data


def process_bank_and_groups(bank_data, credit_dict, debit_dict):
    for txn in bank_data:
        if txn['type'] == 'CREDIT':
            if txn['name'] not in credit_dict:
                credit_dict[txn['name']] = {
                    "group": "TBD",
                    "subGroup": "TBD"
                }
                print(f'{txn["name"]} added to credit dict')
        
        if txn['type'] == 'DEBIT':
            if txn['name'] not in debit_dict:
                debit_dict[txn['name']] = {
                    "group": "TBD",
                    "subGroup": "TBD"
                }
                print(f'{txn["name"]} added to debit dict')

    credit_json_obj = json.dumps(credit_dict, indent=4)
    with open('credit_group_dict.json', 'w') as credit_group_outfile:
        credit_group_outfile.write(credit_json_obj)

    debit_json_obj = json.dumps(debit_dict, indent=4)
    with open('debit_group_dict.json', 'w') as debit_group_outfile:
        debit_group_outfile.write(debit_json_obj)


def pull_group_dict_data():
    with open('credit_group_dict.json') as credit_group_file:
        credit_dict = json.load(credit_group_file)

    with open('debit_group_dict.json') as debit_group_file:
        debit_dict = json.load(debit_group_file)

    return credit_dict, debit_dict


def load(filename):
    credit_dict, debit_dict = pull_group_dict_data()

    with open(f'raw_data/{filename}', mode='r') as bank_csv:
        csv_reader = csv.DictReader(bank_csv)

        if filename.startswith('usbank'):
            bank_data = load_usbank(csv_reader)

        elif filename.startswith('amex'):
            bank_data = load_amex(csv_reader)

        else:
            ValueError('Bank type not found for file')
        
        process_bank_and_groups(bank_data, credit_dict, debit_dict)
