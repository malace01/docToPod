import subprocess
from .logger import logger

command_map = {
    'docker run': 'podman run',
    'docker build': 'podman build',
    'docker ps': 'podman ps',
    'docker stop': 'podman stop',
    'docker rm': 'podman rm',
    # Add more mappings as needed
}

def translate_command(docker_command):
    for docker_cmd, podman_cmd in command_map.items():
        if docker_command.startswith(docker_cmd):
            return docker_command.replace(docker_cmd, podman_cmd, 1)
    return docker_command

def run_command(command):
    translated_command = translate_command(command)
    logger.info(f"Executing: {translated_command}")
    try:
        result = subprocess.run(translated_command.split(), capture_output=True, text=True, check=True)
        logger.info(f"Output: {result.stdout}")
        return result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        logger.error(f"Error: {e.stderr}")
        return "", e.stderr
