###############################################################
# pip install .; pytest -v --capture=no -v --nocapture tests/test_installer.py:Test_installer.test_001
# pytest -v --capture=no tests/test_installerr.py
# pytest -v  tests/test_installer.py
###############################################################

from __future__ import print_function
from invoke import run
import shutil

import os
import pytest

@pytest.mark.incremental
class Test_configdict:

    def test_create_dir(self):
        path = "tmp"
        try:
            os.mkdir(path)
        except OSError:
            print(f"Creation of the directory {path} failed")
        else:
            print(f"Successfully created the directory {path}")

        assert True

    def test_info(self):
        cmd = "cloudmesh-installer info"
        result = run(cmd, hide=True, warn=True)
        print ("status:", result.ok)
        print(result)
        assert result.ok
        assert "Package" in str(result)

    def test_non_existing(self):
        cmd = "cd tmp; cloudmesh-installer git clone WRONG"
        result = run(cmd, hide=True, warn=True)
        assert not result.ok

    def test_clone_community(self):
        cmd = "cd tmp; cloudmesh-installer git clone community"
        result = run(cmd, hide=True, warn=True)
        print ("status:", result.ok)
        print(result)
        assert result.ok
        assert os.path.isdir("tmp/cloudmesh-community.github.io")

    def test_clone_cms(self):
        cmd = "cd tmp; cloudmesh-installer git clone cms"
        result = run(cmd, hide=True, warn=True)
        print ("status:", result.ok)
        print(result)
        assert result.ok
        assert os.path.isdir("tmp/cloudmesh-cmd5")

    def test_clone_install(self):
        cmd = "cd tmp; cloudmesh-installer install cms -e"
        result = run(cmd, hide=True, warn=True)
        print ("status:", result.ok)
        print(result)
        assert result.ok
        assert os.path.isdir("tmp/cloudmesh-cmd5/cloudmesh_cmd5.egg-info")

class other:
    def test_delete_dir(self):
        path = "tmp"
        shutil.rmtree(path)
        assert True
