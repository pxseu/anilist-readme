from subprocess import Popen, PIPE, STDOUT, run

def syscmd(cmd, encoding='', capture_output=False):
    """
    Execute a system command.
    
    Args:
        cmd: Command to execute
        encoding: If provided, decode output with this encoding
        capture_output: If True, capture and return output. If False, pipe to terminal.
    
    Returns:
        If capture_output=True: output string (decoded if encoding provided) or returncode
        If capture_output=False: returncode
    """
    if capture_output:
        # Capture output for commands that need it
        p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT,
            close_fds=True)
        p.wait()
        output = p.stdout.read()
        if len(output) > 1:
            if encoding:
                return output.decode(encoding)
            else:
                return output
        return p.returncode
    else:
        # Pipe to terminal by default
        result = run(cmd, shell=True, stderr=STDOUT)
        return result.returncode