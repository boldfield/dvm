import os

def read_file(file_path, split=False):
    """Read the contents of a file from disk.

       Args:
           file_name (string): full path to file on disk 
    """
    data = None
    if os.path.isfile(file_path):
        with open(file_path, 'r') as fs:
            data = fs.read().strip('\n')
        if split:
            data = data.split('\n')
    return data

def repo_location():
    return os.path.expanduser('~/.dotfiles')

VERSION = read_file(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 'VERSION'))
