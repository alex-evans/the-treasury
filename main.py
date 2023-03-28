import argparse

from src import group_json_creator
from src import group_processor
from src import txn_processor
from src import viewer


def main(args):
    if args.load:
        group_json_creator.load(args.filename)
        return

    if args.group_db:
        group_processor.save_groups_to_db()
        return

    if args.txns:
        txn_processor.save_file(args.filename)
        return

    if args.view:
        date = args.view.split(',')
        year = date[0]
        month = date[1]
        viewer.month_view(int(year), int(month))
        return

    print('Did nothing')


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Handle Treasury.')
    parser.add_argument('-t', '--txns', action='store_true')
    parser.add_argument('-f', '--filename')
    parser.add_argument('-l', '--load', action='store_true')
    parser.add_argument('-g', '--group-db', action='store_true')
    parser.add_argument('-v', '--view')

    args = parser.parse_args()

    main(args)
    