import subprocess
from os.path import abspath, dirname, basename, join
from inspect import getsourcefile

def module_path(local_object):
    '''
    Returns the module path without the use of __file__. Requires a
    function locally defined in the module.

    From:
    http://stackoverflow.com/questions/729583/getting-file-path-of-imported-module
    '''
    path = abspath(getsourcefile(local_object))

    if 'library.zip' == basename(dirname(dirname(path))):
        return join(dirname(dirname(dirname(path))), 'dist')
    else:
        return path

def run_shell_cmd(cmd, gobble_output=True, echo=False):
    if echo:
        print(cmd)
    if gobble_output:
        destination = subprocess.PIPE
    else:
        destination = None
    process = subprocess.Popen(cmd, stdout=destination, stderr=destination, shell=True)
    stdout_str, stderr_str = process.communicate()
    return (stdout_str, stderr_str, process.returncode)
