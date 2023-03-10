import argparse

from src import group_loader
from src import txn_loader
from src import viewer


def main(args):

    if not args.filename:
        viewer.view_treasury()
        return

    if args.load:
        group_loader.load(args.filename)
        return

    txn_loader.load(args.filename)



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-f', '--filename')
    parser.add_argument('-l', '--load', action='store_false')

    args = parser.parse_args()

    main(args)
    
    