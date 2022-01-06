import os

def get_absolute_url(path):
    if os.path.isabs(path):
        return path

    return os.path.abspath(path)

def muiltple_replace(replace_str, replace_dict):
    try:
        print('x')
        if type(replace_str) is str and type(replace_dict) is dict:

            print('x')
            for key, value in replace_dict:
                replace_key = '{{'+ key +'}}'
                print(replace_key)
                if replace_key in value:
                    replace_str.replace(replace_key, value)

            return replace_str
    except Exception as e:
        raise Exception('[Error] Multiple replace parameters type have to be (str, dict): {}'.format(e))

