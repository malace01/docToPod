from setuptools import setup, find_packages

setup(
    name='docker-to-podman',
    version='1.1',
    packages=find_packages(),
    install_requires=[
        'flask',
        'pyyaml',
        'argcomplete',
    ],
    entry_points={
        'console_scripts': [
            'docker-to-podman=docker_to_podman.cli:main',
        ],
    },
)
