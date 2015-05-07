import unittest
from nose.tools import assert_true, assert_equal
from mock import patch, Mock, call

from tests import tmp_repo_path


class TestAdd(unittest.TestCase):
    
    def test_file_names_no_dot(self):
        from dvm import add
        link, filename = add.file_names('bashrc')
        assert_equal(link, '.bashrc')
        assert_equal(filename, 'dot.bashrc.symlink')
    
    def test_file_names_dot(self):
        from dvm import add
        link, filename = add.file_names('.bashrc')
        assert_equal(link, '.bashrc')
        assert_equal(filename, 'dot.bashrc.symlink')
