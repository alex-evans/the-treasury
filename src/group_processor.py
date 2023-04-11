
from dotenv import load_dotenv
import json
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import TxnNames


load_dotenv()
USERNAME = os.environ.get('USERNAME')
PASSWORD = os.environ.get('PASSWORD')
DATABASE = os.environ.get('DATABASE')
engine = create_engine(
    f'postgresql://{USERNAME}:{PASSWORD}@localhost/{DATABASE}'
)
Session = sessionmaker(bind=engine)


def pull_group_dict_data():
    with open('credit_group_dict.json') as credit_group_file:
        credit_dict = json.load(credit_group_file)

    with open('debit_group_dict.json') as debit_group_file:
        debit_dict = json.load(debit_group_file)

    return credit_dict, debit_dict


def update_db(session, group_dict, revenue):

    for group_item in group_dict:

        group_name = group_dict[group_item]['group']
        sub_group_name = group_dict[group_item]['subGroup']

        db_txn_name = session.query(TxnNames)\
                             .filter(TxnNames.name == group_item)\
                             .filter(TxnNames.revenue == revenue)\
                             .filter(TxnNames.group == group_name)\
                             .filter(TxnNames.sub_group == sub_group_name)\
                             .first()

        if db_txn_name:
            continue

        db_txn_name = TxnNames(
                        name=group_item,
                        group=group_dict[group_item]['group'],
                        sub_group=group_dict[group_item]['subGroup'],
                        revenue=revenue                            
                        )
        session.add(db_txn_name)
        print('Added TxnName:', group_item)


def save_groups_to_db():
    print('Running Groups DB')
    session = Session()
    try:
        credit_dict, debit_dict = pull_group_dict_data()

        update_db(session, credit_dict, revenue=True)
        update_db(session, debit_dict, revenue=False)

        session.commit()

    except Exception as e:
        print('Database Failed:', e)
        session.rollback()
