# Docker to Podman Translator
 translates Docker commands to Podman commands and executes them.

## Features

- Command translation from Docker to Podman
- Support for Docker Compose files
- Error logging
- Plugin system for extensibility
- Options for running the tool in a secure environment
- Command autocompletion for CLI

## Installation

To install the package, run:

```bash
pip install .
Usage
Command Line
You can use the tool from the command line:

bash

docker-to-podman "docker run hello-world"


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
```
## CLi ex
docker-to-podman "docker run hello-world"

API version :

python -m docker_to_podman.api
Make a POST request to the /run endpoint with the Docker command:
bash
curl -X POST http://127.0.0.1:5000/run -H "Content-Type: application/json" -d '{"command": "docker run hello-world"}'


 Package and Distribute
Install the Package Locally
To install the package locally, navigate to the root directory of your project and run:

bash
pip install .
b. Create a Distribution
To create a distribution package, you can use setuptools. Run the following command to create a source distribution and a wheel:

bash
python setup.py sdist bdist_wheel
This will create a dist/ directory with the distribution files.
c. Upload to PyPI(idk about if this is allowed or not here?)
If you want to distribute the package via PyPI, you can use twine. First, install twine:

bash

pip install twine
Then, upload the package:

bash

twine upload dist/*
You will need a PyPI account and API token to upload the package


'''

Full Workflow Example
Clone the repository (if applicable):

bash

git clone <repository-url>
cd docker-to-podman
Create a virtual environment (optional but recommended):

bash

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
Install the requirements:

bash

pip install -r requirements.txt
Install the package:

bash

pip install .
Run the command-line tool:

bash

docker-to-podman "docker run hello-world"
Run the Flask API:

bash

python -m docker_to_podman.api
Make a request to the API:

bash

curl -X POST http://127.0.0.1:5000/run -H "Content-Type: application/json" -d '{"command": "docker run hello-world"}'




Configuration
Environment Variables
NON_ROOT_USER: Specify a non-root user to run commands as.
ENFORCE_NON_ROOT: Set to true to enforce running commands as a non-root user.
Plugins
Plugins can be added to the plugins directory. Each plugin should be a Python file with a modify_command function.

Example plugin (plugins/example_plugin.py)
