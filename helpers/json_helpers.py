import json
import os.path


def read_python_object_from_json_file(json_file_name: str) -> object:
    json_file = open(json_file_name)
    json_object = json_file.read()
    json_file.close()
    python_object = json.loads(json_object)
    return python_object


def write_python_object_to_json_file(
        python_object,
        json_generic_file_name: str,
        json_file_path: str,
        timestr: str):
    json_object = json.dumps(python_object, default=vars)
    json_file_name = os.path.join(json_file_path, json_generic_file_name + '_' + timestr + '.json')
    json_object_file = open(file=json_file_name, mode='w')
    json_object_file.write(json_object)
    json_object_file.close()