import os
import subprocess

def run_as_non_root(command):
    non_root_user = os.getenv('NON_ROOT_USER', 'nobody')
    result = subprocess.run(['sudo', '-u', non_root_user] + command.split(), capture_output=True, text=True)
    return result.stdout, result.stderr

def apply_security_measures(command):
    if os.getenv('ENFORCE_NON_ROOT', 'false').lower() == 'true':
        return run_as_non_root(command)
    return subprocess.run(command.split(), capture_output=True, text=True)
