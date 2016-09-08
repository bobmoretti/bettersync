from util.shell import run_shell_cmd, module_path
import os

def run_zsync_make(args = []):
    module_dir = os.path.split(__modpath)[0]
    zs_path = os.path.join(module_dir, 'zsync', 'zsyncmake.exe')
    return run_shell_cmd(zs_path + ' ' + ' '.join(args), echo=True)

__modpath = module_path(run_zsync_make)
