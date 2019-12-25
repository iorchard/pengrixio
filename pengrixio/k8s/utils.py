import ast
import etcd
import random
import socket

from pengrixio.database import etcdc

import logging
import logging.config

from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT
from subprocess import TimeoutExpired

from datetime import datetime

logging.config.fileConfig('logging.conf')
log = logging.getLogger('pengrixio')


def cmd(s_cmd, i_timeout=30, b_sudo=False):
    """Execute s_cmd using Popen.i
    Return:
        t_result: tuple = (
                    b_ret: boolen, cmd return code. 0=True or False
                    s_output: string, json string
                  )
    """
    t_result = (False, {})
    if b_sudo:
        s_cmd = "LANG=C sudo %s" % (s_cmd)

    o_proc = Popen(s_cmd, shell=True, stdout=PIPE, stderr=STDOUT)
    try:
        (B_outs, B_errs) = o_proc.communicate(timeout=i_timeout)
    except TimeoutExpired:
        o_proc.kill()
        (B_outs, B_errs) = o_proc.communicate()

    i_retcode = int(o_proc.returncode)
    b_ret = i_retcode == 0

    s_output = B_outs.decode('utf-8').strip()

    t_result = (b_ret, s_output)

    return t_result

