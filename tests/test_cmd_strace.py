from StringIO import StringIO
import os.path

import mock

from doit.cmdparse import DefaultUpdate
from doit.task import Task
from doit.cmd_strace import Strace


class TestCmdRun(object):

    def test_dep(self, dependency1, depfile):
        output = StringIO()
        task = Task("tt", ["cat %(dependencies)s"],
                    file_dep=['tests/data/dependency1'])
        cmd = Strace(outstream=output)
        cmd._loader.load_tasks = mock.Mock(return_value=([task], {}))
        params = DefaultUpdate(dep_file=depfile.name, show_all=False)
        result = cmd.execute(params, ['tt'])
        assert 0 == result
        got = output.getvalue().split("\n")
        dep_path = os.path.abspath("tests/data/dependency1")
        assert "R %s" % dep_path in got[0]


    def test_show_all(self, dependency1, depfile):
        output = StringIO()
        task = Task("tt", ["cat %(dependencies)s"],
                    file_dep=['tests/data/dependency1'])
        cmd = Strace(outstream=output)
        cmd._loader.load_tasks = mock.Mock(return_value=([task], {}))
        params = DefaultUpdate(dep_file=depfile.name, show_all=True)
        result = cmd.execute(params, ['tt'])
        assert 0 == result
        got = output.getvalue().split("\n")
        assert "cat" in got[0]


    def test_target(self, dependency1, depfile):
        output = StringIO()
        task = Task("tt", ["touch %(targets)s"],
                    targets=['tests/data/dependency1'])
        cmd = Strace(outstream=output)
        cmd._loader.load_tasks = mock.Mock(return_value=([task], {}))
        params = DefaultUpdate(dep_file=depfile.name, show_all=False)
        result = cmd.execute(params, ['tt'])
        assert 0 == result
        got = output.getvalue().split("\n")
        tgt_path = os.path.abspath("tests/data/dependency1")
        assert "W %s" % tgt_path in got[0]