import os
import unittest
from nose.tools import assert_true, assert_equal
from mock import patch, Mock, call

from tests import tmp_repo_path


class TestRepo(unittest.TestCase):

    @patch('dvm.repo.git.Repo')
    def test_init_no_origin(self, MockRepo):
        from dvm import repo
        with tmp_repo_path() as target:
            with patch.object(os, 'mkdir') as mock_mkdir:
                repo.init(target)
                MockRepo.init.assert_called_once_with(target)
                mock_mkdir.assert_called_once_with(os.path.join(target, 'rc'))

    @patch('dvm.repo.git.Repo')
    def test_init_with_origin(self, MockRepo):
        from dvm import repo
        exp_origin = 'git@example.com:user/dfiles.git'

        mock_repo = Mock()
        MockRepo.init.return_value = mock_repo

        with tmp_repo_path() as target:
            with patch.object(os, 'mkdir') as mock_mkdir:
	        repo = repo.init(target, origin=exp_origin)

                MockRepo.init.assert_called_once_with(target)
                mock_repo.create_remote.assert_called_once_with('origin', exp_origin)
                repo.remotes.origin.pull.assert_called_once_with('master')

    def test_add_untracked(self):
        from dvm import repo
        exp_msg = 'Adding files'
        untracked = ['dot.vimrc', 'dot.bashrc', 'dot.bash_profile']
        mock_repo = Mock()
        mock_repo.untracked_files = untracked
        repo.add_all_new(mock_repo, exp_msg)
        mock_repo.index.add.assert_has_calls([call(f) for f in untracked])
        assert_equal(mock_repo.index.add.call_count, len(untracked))
