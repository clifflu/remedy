# -*- coding: utf8 -*-

from fabric.api import *

class Result(object):
    """> 0 for successive results, < 0 otherwise"""
    S_NO_NEED = 1
    S_I_PATCH = 10
    F_LOGIN = -2
    F_SUDO = -18
    F_LAG_REPO = -27
    F_OTHER = -41

    @classmethod
    def s(cls, msg):
        return (getattr(cls, msg), msg[2:])


bash_ok = [
    'bash-3.2-33',
    'bash-4.1.2'
]

env.abort_on_prompts = True
env.abort_exception = Exception

def cure(host):
    env.host_string = host

    with hide('output', 'running', 'warnings', 'aborts'), settings(warn_only=True):
        def ok():
            v = run("rpm -qa | grep bash", stdout = None, stderr=None)

            for ok in bash_ok:
                try: v.index(ok)
                except ValueError:
                    continue
                return True
            return False

        try:
            if ok(): return Result.s("S_NO_NEED")
        except KeyboardInterrupt as e: raise e
        except:
            return Result.s("F_LOGIN")

        try:
            sudo("if [ -x `which yum` ]; then yum update bash -y > /dev/null; elif [ -x `which apt-get` ]; then apt-get upgrade bash -y > /dev/null; fi", stdout=None, stderr=None)
        except KeyboardInterrupt as e: raise e
        except Exception as e:
            return Result.s("F_SUDO")

        try:
            return Result.s("S_I_PATCH") if ok() else Result.s("F_LAG_REPO")
        except KeyboardInterrupt as e: raise e
        except:
            return Result.s("F_LOGIN")

        return Result.s("F_OTHER")
