import yaml

def translate_compose_file(docker_compose_file):
    with open(docker_compose_file, 'r') as file:
        docker_compose = yaml.safe_load(file)
    
    podman_compose = docker_compose  # Simple translation for now; customize as needed
    
    podman_compose_file = docker_compose_file.replace('docker-compose', 'podman-compose')
    with open(podman_compose_file, 'w') as file:
        yaml.safe_dump(podman_compose, file)
    
    return podman_compose_file

def run_compose_command(compose_file, command):
    podman_compose_file = translate_compose_file(compose_file)
    result = subprocess.run(['podman-compose', command, '-f', podman_compose_file], capture_output=True, text=True)
    return result.stdout, result.stderr
