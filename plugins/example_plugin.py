def modify_command(command):
    # Example: add a custom flag to all run commands
    if command.startswith('podman run'):
        command += ' --custom-flag'
    return command
