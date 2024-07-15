

# Docker to Podman Translator
 translates Docker commands to Podman commands and executes them, with a web interface now!

## Features

- Command translation from Docker to Podman
- Support for Docker Compose files
- Error logging
- Plugin system for extensibility
- Options for running the tool in a secure environment
- Command autocompletion for CLI
- Multi-user support with authentication
- Web interface for command execution
- File upload for Docker Compose files

## Installation

To install the package, run:

```bash
pip install .
Usage
Command Line
You can use the tool from the command line:

bash

docker-to-podman docker "docker run hello-world"
Docker Compose
To translate and run Docker Compose files, use:

bash

docker-to-podman compose path/to/docker-compose.yml up
Autocompletion
To enable autocompletion, add the following line to your shell configuration file (e.g., .bashrc or .zshrc):

bash

eval "$(register-python-argcomplete docker-to-podman)"
Then, source the configuration file:

bash

source ~/.bashrc  # or ~/.zshrc
API
You can also use the tool as a REST API with basic authentication:

bash

python -m docker_to_podman.api
Make a POST request to the /run endpoint with the Docker command:

bash

curl -u admin:password123 -X POST http://127.0.0.1:5000/run -H "Content-Type: application/json" -d '{"command": "docker run hello-world"}'
Web Interface
You can use the tool through a web interface with basic authentication:

bash

python -m docker_to_podman.web
Visit http://127.0.0.1:5000 in your web browser and log in with your credentials.

Upload Docker Compose File
To upload a Docker Compose file and execute commands on it, visit http://127.0.0.1:5000/upload in your web browser.

Configuration
Environment Variables
NON_ROOT_USER: Specify a non-root user to run commands as.
ENFORCE_NON_ROOT: Set to true to enforce running commands as a non-root user.


Plugins
Plugins can be added to the plugins directory. Each plugin should be a Python file with a modify_command function.

Example plugin (plugins/example_plugin.py)
Logging
Logs are written to docker_to_podman.log.
