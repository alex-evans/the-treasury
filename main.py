import rich_click as click

from src import load_csv
from src import view


@click.group()
def cli():
    pass


@cli.command()
@click.argument('path', type=click.Path(), required=True)
def load(path):
    '''Load Bank CSV file'''
    print('Path:', path)


if __name__ == '__main__':
    cli()