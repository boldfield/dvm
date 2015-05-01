import os
import tempfile
import shutil
import contextlib


@contextlib.contextmanager
def tmp_repo_path(name=None):
    name = name or 'dfiles'
    tdir = tempfile.mkdtemp()
    try:
        yield os.path.join(tdir, name) 
    finally:
        shutil.rmtree(tdir)
