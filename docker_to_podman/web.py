# docker_to_podman/web.py

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_httpauth import HTTPBasicAuth
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import subprocess
from .translator import translate_command
from .logger import logger
from .plugins import load_plugins, apply_plugins
from .security import apply_security_measures

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
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

if __name__ == '__main__':
    app.run(debug=True)
