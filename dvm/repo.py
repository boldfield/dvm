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
    return repo

def add_origin(repo, origin):
    """Add a remote origin to existing repository.
    """
    repo.create_remote('origin', origin)
    repo.remotes.origin.fetch()

def add_all_new(repo, mgs):
    for new in repo.untracked_files:
        repo.index.add(new)
    repo.index.commit(new)

def _init_paths(path, repo):
    for d in ['rc']:
        path = os.path.join(path, 'rc')
        os.mkdir(path)
