import os
import sys

import sh


def start(name):
    pwd = sh.pwd(_out=sys.stdout)

    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(path, "server")

    sh.cd(path)
    sh.docker_compose("up", "-d", name, _out=sys.stdout)
    sh.docker_compose("up", "waiter", _out=sys.stdout)
    sh.cd(pwd)


def stop(name):
    pwd = sh.pwd(_out=sys.stdout)

    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(path, "server")

    sh.cd(path)
    sh.docker_compose("rm", "--force", "--stop", name, _out=sys.stdout)
    sh.cd(pwd)
