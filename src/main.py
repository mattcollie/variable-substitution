import json
import os
import logging
import re
import sys


def main(files: list[str] | str):
    logging.basicConfig(level=logging.DEBUG)

    if isinstance(files, str):
        files = [files]

    for file in files:
        try:
            logging.info(f'Processing file: {file}')
            with open(file, 'r') as f:
                data = json.load(f)

            for key, value in data.items():
                data = process_item(key, value, data)

            with open(file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logging.warning(f'Failed to process file: {file}; {e}')


def process_item(key, value, data) -> dict:
    if isinstance(value, str):
        regex_pattern = r"\$\{\{\s*([A-Z0-9_]+)\s*\}\}"

        matches = re.findall(regex_pattern, value)

        for var_name in matches:
            env_value = os.environ.get(var_name)
            if env_value:
                value = re.sub(rf"\$\{{\{{\s*{var_name}\s*\}}\}}", env_value, value)
                data[key] = value
            else:
                logging.warning(f"Warning: Environment variable '{var_name}' not found")
    elif isinstance(value, list):
        for v in value:
            process_item(None, v, value)
    elif isinstance(value, dict):
        for k, v in value.items():
            value = process_item(k, v, value)
    return data


if __name__ == '__main__':
    input_files = os.environ.get('INPUT_FILES')  # Read from environment
    if input_files:
        files_to_process = input_files.split(',')
        main(files_to_process)
    else:
        print("Error: Missing input 'files'.")
        sys.exit(1)
