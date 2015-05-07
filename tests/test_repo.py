import os
import unittest
from nose.tools import assert_true, assert_equal
from mock import patch, Mock, MagicMock, call

from tests import tmp_repo_path


class TestRepo(unittest.TestCase):

    @patch('dvm.repo.git.Repo')
    def test_init_no_origin(self, MockRepo):
        with patch('dvm.repo.open', create=True) as mock_open:
	  mock_open.return_value = MagicMock(spec=file)
          from dvm import repo
          with tmp_repo_path() as target:
              with patch.object(os, 'mkdir') as mock_mkdir:
                  repo.init(target)
                  MockRepo.init.assert_called_once_with(target)
                  mock_mkdir.assert_has_calls([call(os.path.join(target, 'rc')), call(os.path.join(target, 'source'))])
                  mock_open.assert_any_call(os.path.join(target, 'source', 'alias.sh'), 'w')
                  mock_open.assert_any_call(os.path.join(target, 'source', 'environment.sh'), 'w')

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
        untracked = ['dot.vimrc.symlink', 'dot.bashrc.symlink', 'dot.bash_profile.symlink']
        mock_repo = Mock()
        mock_repo.untracked_files = untracked
        repo.add_all_new(mock_repo, exp_msg)
        mock_repo.index.add.assert_has_calls(call(untracked))
        assert_equal(mock_repo.index.add.call_count, 1)

    @patch('dvm.repo.repo_location')
    @patch('dvm.repo.git.Repo')
    def test_get_repo(self, MockRepo, mock_loc):
        with tmp_repo_path() as target:
            mock_loc.return_value = target
            from dvm import repo
            mock_repo = repo.get_repo()
            MockRepo.assert_called_once_with(target)

    @patch('dvm.repo.repo_location')
    def test_file_path(self, mock_loc):
        with tmp_repo_path() as target:
            mock_loc.return_value = target
            from dvm import repo

            fpath_rc = repo.file_path('test.sh')
            assert_equal(fpath_rc, os.path.join(target, 'rc', 'test.sh'))

            fpath_source = repo.file_path('test2.sh', 'source')
            assert_equal(fpath_source, os.path.join(target, 'source', 'test2.sh'))
