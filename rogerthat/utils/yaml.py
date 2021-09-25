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


def yml_clear_list(the_list):
    new_list = ruamel.yaml.comments.CommentedSeq(the_list)
    new_list.clear()
    new_list._yaml_comment = the_list.ca
    return new_list


def yml_fix_list_comments(the_list):
    if len(list(the_list.ca.items.keys())):
        new_comment_key = list(the_list.ca.items.keys())[0]
        the_list.ca.items[int(len(the_list) - 1)] = the_list.ca.items.pop(new_comment_key)
    return the_list


def yml_add_to_list(the_list, new_val):
    the_list.append(new_val)
    yml_fix_list_comments(the_list)
    return the_list
