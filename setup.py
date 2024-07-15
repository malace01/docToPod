from setuptools import setup, find_packages

setup(
    name='docker-to-podman',
    version='1.1',  # Updated version
    packages=find_packages(),
    install_requires=[
        'flask',
        'pyyaml',  # Added dependency
    ],
    entry_points={
        'console_scripts': [
            'docker-to-podman=docker_to_podman.translator:run_command',
        ],
    },
)
