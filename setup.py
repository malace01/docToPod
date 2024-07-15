# setup.py

from setuptools import setup, find_packages

setup(
    name='docker-to-podman',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'flask',
    ],
    entry_points={
        'console_scripts': [
            'docker-to-podman=docker_to_podman.translator:run_command',
        ],
    },
)
