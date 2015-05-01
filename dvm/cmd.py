"""dotfile version manager (dvm-%s)

Usage:
    dvm init [--origin=<origin>]

Options:
    --origin=<origin>  The remote origin to use for the local dotfiles repo.
                       If set at initialization time, the remote repo will be
                       pulled in.

"""
from docopt import docopt

from dvm import repo
from dvm.util import read_file, VERSION


def main():
    args = docopt(__doc__ % VERSION, version='dvm {}'.format(VERSION))
    if args['init']:
        repo.cmd_init(args)

