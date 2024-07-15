import importlib
import os

PLUGINS_DIR = 'plugins'

def load_plugins():
    plugins = []
    for filename in os.listdir(PLUGINS_DIR):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = filename[:-3]
            module = importlib.import_module(f'{PLUGINS_DIR}.{module_name}')
            plugins.append(module)
    return plugins

def apply_plugins(command, plugins):
    for plugin in plugins:
        command = plugin.modify_command(command)
    return command
