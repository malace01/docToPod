# docker_to_podman/api.py

from flask import Flask, request, jsonify
import subprocess
from .translator.py import translate_command

app = Flask(__name__)

@app.route('/run', methods=['POST'])
def run_command():
    docker_command = request.json.get('command')
    translated_command = translate_command(docker_command)
    result = subprocess.run(translated_command.split(), capture_output=True, text=True)
    return jsonify({
        'stdout': result.stdout,
        'stderr': result.stderr
    })

if __name__ == '__main__':
    app.run(debug=True)
