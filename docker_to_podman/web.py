# docker_to_podman/web.py

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_httpauth import HTTPBasicAuth
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename
import os
import subprocess
from .translator import translate_command
from .compose_translator import run_compose_command
from .dockerfile_translator import translate_dockerfile
from .logger import logger
from .plugins import load_plugins, apply_plugins
from .security import apply_security_measures

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'yml', 'yaml', 'Dockerfile'}
auth = HTTPBasicAuth()

# Example user data
users = {
    "admin": "password123",
    "user": "password"
}

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username

plugins = load_plugins()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

class CommandForm(FlaskForm):
    command = StringField('Docker Command', validators=[DataRequired()])
    submit = SubmitField('Execute')

@app.route('/', methods=['GET', 'POST'])
@auth.login_required
def index():
    form = CommandForm()
    output = None
    error = None
    if form.validate_on_submit():
        docker_command = form.command.data
        translated_command = translate_command(docker_command)
        translated_command = apply_plugins(translated_command, plugins)
        logger.info(f"{auth.current_user()} executing: {translated_command}")
        try:
            result = apply_security_measures(translated_command)
            logger.info(f"Output: {result[0]}")
            output = result[0]
            error = result[1]
        except subprocess.CalledProcessError as e:
            logger.error(f"Error: {e.stderr}")
            error = e.stderr
    return render_template('index.html', form=form, output=output, error=error)

@app.route('/upload', methods=['GET', 'POST'])
@auth.login_required
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            flash('File successfully uploaded')
            if filename == 'Dockerfile':
                return redirect(url_for('translate_dockerfile', filename=filename))
            else:
                return redirect(url_for('execute_compose', filename=filename))
    return render_template('upload.html')

@app.route('/translate_dockerfile/<filename>', methods=['GET', 'POST'])
@auth.login_required
def translate_dockerfile_view(filename):
    dockerfile_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    podmanfile_path = translate_dockerfile(dockerfile_path)
    with open(podmanfile_path, 'r') as file:
        podmanfile_content = file.read()
    return render_template('translate_dockerfile.html', podmanfile_content=podmanfile_content)

@app.route('/build_and_run/<filename>', methods=['GET', 'POST'])
@auth.login_required
def build_and_run(filename):
    podmanfile_path = os.path.join(app.config['UPLOAD_FOLDER'], filename.replace('Dockerfile', 'Podmanfile'))
    image_name = filename.replace('Dockerfile', '').lower()
    try:
        # Build the image using Podman
        build_command = f'podman build -t {image_name} -f {podmanfile_path}'
        build_result = subprocess.run(build_command.split(), capture_output=True, text=True, check=True)
        build_output = build_result.stdout

        # Run the container using Podman
        run_command = f'podman run {image_name}'
        run_result = subprocess.run(run_command.split(), capture_output=True, text=True, check=True)
        run_output = run_result.stdout

        output = build_output + "\n" + run_output
        error = ""
    except subprocess.CalledProcessError as e:
        output = ""
        error = e.stderr

    return render_template('build_and_run.html', output=output, error=error)

@app.route('/execute_compose/<filename>', methods=['GET', 'POST'])
@auth.login_required
def execute_compose(filename):
    compose_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    output, error = run_compose_command(compose_file_path, 'up')
    return render_template('execute_compose.html', output=output, error=error)

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
