import click
import sys

def info(msg):
    """standard info call"""
    click.secho(msg.strip(), fg='green')


def echo(msg):
    """standard echo call"""
    click.secho(msg.strip(), fg='blue')


def warning(msg):
    click.secho('WARN: {}'.format(msg.strip()), fg='magenta')


def error(msg, error_code=-1):
    """standard error call"""
    click.secho("ERROR: {}".format(msg.strip()), fg='red')
    sys.exit(error_code)
