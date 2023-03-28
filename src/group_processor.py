
from dotenv import load_dotenv
import json
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from models import Groups
from models import SubGroups
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


def update_db(session, group_dict):
    for group_item in group_dict:
        
        # Group
        group = group_dict[group_item]['group']
        db_group = session.query(Groups).filter(Groups.name == group).first()
        if not db_group:
            db_group = Groups(
                        name=group
                       )
            session.add(db_group)
            print('Added Group:', group)

        # Sub Group
        sub_group = group_dict[group_item]['subGroup']
        db_sub_group = session.query(SubGroups).filter(SubGroups.name == sub_group).first()
        if not db_sub_group:
            db_sub_group = SubGroups(
                            name=sub_group,
                            group=db_group
                           )
            session.add(db_sub_group)
            print('Added SubGroup', sub_group)
        else:
            db_sub_group.group = db_group

        # Txn Name
        db_txn_name = session.query(TxnNames).filter(TxnNames.name == group_item).first()
        if not db_txn_name:
            db_txn_name = TxnNames(
                            name=group_item,
                            sub_group=db_sub_group
                          )
            session.add(db_txn_name)
            print('Added TxnName:', group_item)
        else:
            db_txn_name.sub_group = db_sub_group


def save_groups_to_db():
    print('Running Groups DB')
    session = Session()
    try:
        credit_dict, debit_dict = pull_group_dict_data()

        update_db(session, credit_dict)
        update_db(session, debit_dict)

        session.commit()
        
    except Exception as e:
        print('Database Failed:', e)
        session.rollback()
