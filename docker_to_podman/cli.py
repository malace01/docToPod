import argcomplete
import argparse
from .translator import run_command
from .compose_translator import run_compose_command

def main():
    parser = argparse.ArgumentParser(description="Docker to Podman Translator")
    subparsers = parser.add_subparsers(dest="subcommand", help="Subcommands")

    # Subcommand for regular Docker commands
    docker_parser = subparsers.add_parser("docker", help="Translate and run Docker commands")
    docker_parser.add_argument("command", help="Docker command to translate and execute")

    # Subcommand for Docker Compose commands
    compose_parser = subparsers.add_parser("compose", help="Translate and run Docker Compose commands")
    compose_parser.add_argument("compose_file", help="Path to the Docker Compose file")
    compose_parser.add_argument("compose_command", help="Docker Compose command to execute")

    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    if args.subcommand == "docker":
        stdout, stderr = run_command(args.command)
    elif args.subcommand == "compose":
        stdout, stderr = run_compose_command(args.compose_file, args.compose_command)

    if stdout:
        print("Output:", stdout)
    if stderr:
        print("Error:", stderr)

if __name__ == "__main__":
    main()
