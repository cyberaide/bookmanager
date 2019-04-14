###############################################################
# pip install .; pytest -v --capture=no -v --nocapture tests/test_installer.py:Test_bookmanager.test_001
# pytest -v --capture=no tests/test_bookmanagerr.py
# pytest -v  tests/test_bookmanager.py
###############################################################

from __future__ import print_function
import shutil

import os
import pytest
from cloudmesh_installer.install.test import readfile, run


@pytest.mark.incremental
class Test_bokmenager:

    def test_python_book(self):
        cmd = "bookmanager test/python.yaml get"
        result = run(cmd)
        print(result)

        cmd = "ls"
        result = run(cmd)
        print(result)

        cmd = "ls dest"
        result = run(cmd)
        print(result)

        assert os.path.exists("dest/vonLaszewski-python.epub") == 1
