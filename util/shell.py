def run_shell_cmd(cmd, gobble_output=True, echo=False):
    if echo:
        print cmd

    if gobble_output:
        destination = subprocess.PIPE
    else:
        destination = None

    process = subprocess.Popen(cmd, stdout=destination, stderr=destination, shell=True)

    stdout_str, stderr_str = process.communicate()
    
    return (stdout_str, stderr_str, process.returncode)
