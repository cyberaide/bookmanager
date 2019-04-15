###############################################################
# pip install .; pytest -v --capture=no -v --nocapture tests/test_installer.py:Test_bookmanager.test_001
# pytest -v --capture=no tests/test_bookmanagerr.py
# pytest -v  tests/test_bookmanager.py
###############################################################

from __future__ import print_function
import shutil

import os
import pytest
from bookmanager.run import run
from cloudmesh.common.util import readfile
from cloudmesh.DEBUG import VERBOSE

@pytest.mark.incremental
class Test_bokmenager:

    def test_find_python_yml(self):
        cmd = "ls tests".split(" ")
        result = run(cmd)
        VERBOSE(result)
        assert "python.yml" in result.stdout


    def test_python_book(self):

        cmd = "bookmanager tests/python.yml get".split(" ")
        result = run(cmd)
        VERBOSE(result)
        assert True

    def test_check_for_output(self):
        cmd = "ls dest".split(" ")
        result = run(cmd)
        VERBOSE(result)

        assert os.path.exists("./dest/vonLaszewski-python.epub") == 1
