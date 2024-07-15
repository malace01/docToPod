import subprocess
from .logger import logger
from .plugins import load_plugins, apply_plugins
from .security import apply_security_measures

command_map = {
    'docker run': 'podman run',
    'docker build': 'podman build',
    'docker ps': 'podman ps',
    'docker stop': 'podman stop',
    'docker rm': 'podman rm',
    # Add more mappings as needed
}

plugins = load_plugins()

def translate_command(docker_command):
    for docker_cmd, podman_cmd in command_map.items():
        if docker_command.startswith(docker_cmd):
            return docker_command.replace(docker_cmd, podman_cmd, 1)
    return docker_command

def run_command(command):
    translated_command = translate_command(command)
    translated_command = apply_plugins(translated_command, plugins)
    logger.info(f"Executing: {translated_command}")
    try:
        result = apply_security_measures(translated_command)
        logger.info(f"Output: {result[0]}")
        return result
    except subprocess.CalledProcessError as e:
        logger.error(f"Error: {e.stderr}")
        return "", e.stderr
