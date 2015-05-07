import os
import ntpath
import shutil
from mock import MagicMock

from dvm import repo


def cmd_add(args):
    add_fpath = args['<file>']
    if not os.path.isabs(add_fpath):
        add_fpath = os.path.abspath(add_fpath)
    if args['--link-name'] is not None:
        add_filename = args['--link-name']
    else:
        add_filename = ntpath.basename(add_fpath)
    linkname, filename = file_names(add_filename)
    local_repo = repo.get_repo()
    add_file(local_repo, add_fpath, filename, linkname)

def add_file(local_repo, source_path, dest_fname, link_fname):
    """Add a file to the dotfiles repo.  Returns boolean indicating if the
    file was successfully added or not.

    Args:
        local_repo (git.Repo):      local dotfiles repo instance
        source_path (string): full path to file which is to be added to the
                              dotfiles repo
        dest_fname (string):  filename for the file which should be added to
                              the dotfiles repo
        link_fname (string):  filename for link which should be created
    """
    link_path = os.path.expanduser('~/{}'.format(link_fname))
    dest_path = repo.file_path(dest_fname)

    if not _do_proceed(link_path):
        return False

    if link_path == source_path:
        action = shutil.move
    else:
        action = shutil.copyfile

    action(source_path, dest_path)
    if os.path.isfile(link_path):
        shutil.os.remove(link_path)

    os.symlink(dest_path, link_path)
    repo.add_all_new(local_repo, 'Adding {} to dotfiles'.format(ntpath.basename(dest_path)))
    return True

def file_names(inp_fname):
    """Return the linkname and filename for dotfile based on user input.
    """
    link = inp_fname if inp_fname.startswith('.') else ".{}".format(inp_fname)
    return link, "dot{}.symlink".format(link)

def _do_proceed(fpath):
    if os.path.isfile(fpath):
        msg = 'The file {} already exists and will be overwritten. Continue? (y/[n]) '
        cont = raw_input(msg.format(fpath))
        if not cont.strip().lower() == 'y':
            return False
    return True
