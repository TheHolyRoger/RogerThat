import ruamel.yaml


def load_yml_from_file(file_path):
    yaml = ruamel.yaml.YAML()
    Data = None
    with open(file_path) as file:
        Data = yaml.load(file)
    return Data


def save_yml_to_file(data, file_path):
    yaml = ruamel.yaml.YAML()
    with open(file_path, "w") as file:
        yaml.dump(data, file)
    return True
