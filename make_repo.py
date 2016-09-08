from glob import glob
import os
from zsync_wrapper import run_zsync_make

def get_file_list(root_dir):
    file_list = glob(os.path.join(root_dir, '**'), recursive=True)
    return [os.path.abspath(path) for path in file_list if os.path.isfile(path)]

def make_repo(root_dir, output_dir):
    root_dir = os.path.abspath(root_dir)
    files = get_file_list(root_dir)
    print(root_dir)
    outpath = os.path.join(output_dir, '.bsync')
    if not os.path.exists(outpath):
        os.makedirs(outpath)

    for f in files:
        rel_path = f[len(root_dir) + len(os.path.sep):]
        outfile = os.path.join(outpath, rel_path + '.zsync')
        dname, fname  = os.path.split(outfile)
        nesting_level = len(dname.split(os.path.sep)) - 1
        if not os.path.exists(dname):
            os.makedirs(dname)
        rel_url = '../'*nesting_level + '/'.join(rel_path.split('\\'))
        x = run_zsync_make(['-u', rel_url, '-o', outfile, f])

