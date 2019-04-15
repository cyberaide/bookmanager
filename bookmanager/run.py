import subprocess
import sys
from cloudmesh.common.dotdict import dotdict
import os
from cloudmesh.DEBUG import VERBOSE


def run(cmd):
    out = dotdict({
        "stdout": None,
        "stderr": None,
        "code": None,

    })
    os.environ['PYTHONUNBUFFERED'] = "1"
    proc = subprocess.Popen(cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            )
    proc.wait()
    out.stdout, out.stderr = proc.communicate()
    out.code = proc.returncode

    if out.stderr is not None:
        out.stderr = out.stderr.decode("utf-8")

    if out.stdout is not None:
        out.stdout = out.stdout.decode("utf-8")

    return out
