import json
from flask import jsonify
import configparser

request="gimme" # A dummy global variable typically from flask

# A dummy function stub
def session_validate_token(request):
    return True,"user",None

# A dummy function stub
def configuration_file_filename_to_fullpath(filename):
    return "px.ini"

def configuration_file_get(filename=""):
    validated, username, validation_error = session_validate_token(request)
    if not validated:
        return jsonify(validation_error), 401

    config = configparser.RawConfigParser()

    file = configuration_file_filename_to_fullpath(filename)
    with open(file, 'r') as ini_file:
        lines = ini_file.readlines()

    data = {}
    current_section = None
    current_comment = None

    for line in lines:
        line = line.strip()

        if line.startswith('#') or line.startswith(';'):
            if current_comment is None:
                current_comment = []
            current_comment.append(line[1:].strip())
            continue
        # print(current_comment)
        if line.startswith('[') and line.endswith(']'):
            if current_section:
                data[current_section]['__comment'] = current_comment

            current_section = line[1:-1]
            data[current_section] = {}
            current_comment = None
            continue

        if '=' in line:
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip()
            if current_comment:
                data[current_section][key] = {
                    'value': value,
                    'comment': current_comment
                }
                current_comment = None
            else:
                if current_section:
                    data[current_section][key] = value

    if current_section:
        data[current_section]['__comment'] = current_comment

    json_data = json.dumps(data, indent=4)
    return json_data


json=configuration_file_get("px.ini")
print(json)