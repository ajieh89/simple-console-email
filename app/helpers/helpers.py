import os

def get_absolute_url(path):
    if os.path.isabs(path):
        return path

    return os.path.abspath(path)

def multiple_replace(string, replace_dict):
    for  key, value in replace_dict.items():
        string = string.replace('{{' + key.upper() + '}}', str(value))

    return string