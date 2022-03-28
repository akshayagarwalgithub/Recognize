from utils.get_project_root import get_project_root
import json

def get_configuration():
    root_dir=get_project_root()
    with open(root_dir / 'conf' / 'config.json') as json_conf_file:
        conf_variables = json.load(json_conf_file)
    return conf_variables