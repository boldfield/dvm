"""
Dotfiel repo management utilities.
"""
import os
import git

from dvm.util import repo_location


def cmd_init(args):
    """Commandline interface to dotfile repo initialization.
    """
    loc = repo_location()
    init(loc, origin=args['--origin'])

def cmd_add_origin(args):
    """Commandline interface to add origin to dotfile repo.
    """
    loc = repo_location()
    repo = git.Repo.init(path)
    add_origin(repo, args['<origin>'])

def init(path, origin=None):
    """Initialize dotfile repository in `path`. Optionally set
    upstream remote and pull in any existing configuration.
    """
    repo = git.Repo.init(path)
    if origin is not None:
        add_origin(repo, origin)
        repo.remotes.origin.pull('master')
    else:
        _init_paths(path, repo)
        add_all_new(repo, 'Initializing new dotfiles repo')
    return repo

def add_origin(repo, origin):
    """Add a remote origin to existing repository.
    """
    repo.create_remote('origin', origin)
    repo.remotes.origin.fetch()

def add_all_new(repo, msg):
    repo.index.add(repo.untracked_files)
    repo.index.commit(msg)

def get_repo():
    loc = repo_location()
    return git.Repo(loc)

def file_path(fname, folder='rc'):
    loc = repo_location()
    return os.path.join(loc, folder, fname)

def _init_paths(path, repo):
    for d in ['rc', 'source']:
        mk_path = os.path.join(path, d)
        os.mkdir(mk_path)
    for f in ['alias.sh', 'environment.sh']:
        mk_path = os.path.join(path, 'source', f)
        with open(mk_path, 'w') as fs:
            fs.write('#!/usr/bin/env sh\n')
