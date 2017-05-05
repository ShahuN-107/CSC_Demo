import os
from pathlib import Path

BASE_DIR = os.path.dirname(__file__)
PLUGIN_DIR = os.path.join(BASE_DIR, 'plugins')
plugin_names = []
configs = []

cnt = 0


def get_plugins_dict():
    plugin_dict = {}

    for path, dirs, files in os.walk(PLUGIN_DIR):

        if len(files) != 0:
            file_loc = Path(os.path.join(path, 'config.txt'))

            if file_loc.is_file():
                settings_dict = {}

                with open(file_loc, "r") as file:

                    for row in file:
                        _row = row.rstrip().split('=')
                        settings_dict[_row[0]] = _row[1]

                plugin_dict[str(os.path.basename(os.path.normpath(path)))] = settings_dict

    return plugin_dict


if __name__ == "__main__":
    plugin_dict = get_plugins_dict()
