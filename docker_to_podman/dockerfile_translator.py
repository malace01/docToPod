# docker_to_podman/dockerfile_translator.py

import re

# Define mappings for Dockerfile instructions to Podman equivalents
instruction_map = {
    'FROM': 'FROM',
    'RUN': 'RUN',
    'CMD': 'CMD',
    'LABEL': 'LABEL',
    'MAINTAINER': 'MAINTAINER',
    'EXPOSE': 'EXPOSE',
    'ENV': 'ENV',
    'ADD': 'ADD',
    'COPY': 'COPY',
    'ENTRYPOINT': 'ENTRYPOINT',
    'VOLUME': 'VOLUME',
    'USER': 'USER',
    'WORKDIR': 'WORKDIR',
    'ARG': 'ARG',
    'ONBUILD': 'ONBUILD',
    'STOPSIGNAL': 'STOPSIGNAL',
    'HEALTHCHECK': 'HEALTHCHECK',
    'SHELL': 'SHELL',
    # Add more mappings as needed
}

def translate_dockerfile(dockerfile_path):
    with open(dockerfile_path, 'r') as file:
        dockerfile_content = file.readlines()
    
    podmanfile_content = []
    
    for line in dockerfile_content:
        # Match the Dockerfile instruction
        match = re.match(r'^\s*(\w+)', line)
        if match:
            instruction = match.group(1)
            podman_instruction = instruction_map.get(instruction, instruction)
            translated_line = line.replace(instruction, podman_instruction, 1)
            podmanfile_content.append(translated_line)
        else:
            podmanfile_content.append(line)
    
    podmanfile_path = dockerfile_path.replace('Dockerfile', 'Podmanfile')
    with open(podmanfile_path, 'w') as file:
        file.writelines(podmanfile_content)
    
    return podmanfile_path
