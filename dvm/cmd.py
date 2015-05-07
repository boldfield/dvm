"""dotfile version manager (dvm-%s)

Usage:
    dvm init [--origin=<origin>]
    dvm add-origin <origin>
    dvm add <file> [--link-name=<link-name>]

Options:
    --origin=<origin>        The remote origin to use for the local dotfiles repo.
                             If set at initialization time, the remote repo will be
                             pulled in.
    --link-name=<link-name>  The file name of the link to be created in $HOME, eg
                             `.bashrc`

"""
from docopt import docopt

from dvm import repo, add
from dvm.util import read_file, VERSION


def main():
    args = docopt(__doc__ % VERSION, version='dvm {}'.format(VERSION))
    if args['init']:
        repo.cmd_init(args)
    elif args['add-origin']:
        repo.cmd_add_origin(args)
    elif args['add']:
        add.cmd_add(args)

