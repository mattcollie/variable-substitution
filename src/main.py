import json
import logging
import os
import re
import sys


def main(file: str):
    try:
        if not os.path.isfile(file):
            logging.critical(f"'{file}' does not exist.")
            sys.exit(1)

        logging.info(f"Processing file: {file}")
        with open(file, "r") as f:
            data = json.load(f)

        for key, value in data.items():
            data = process_item(key, value, data)

        with open(file, "w") as f:
            json.dump(data, f, indent=2)

        with open(file, "r") as f:
            data = json.load(f)

        check_for_unsubstituted_variables(data)
        logging.info(f"All variables substituted successfully for: {file}!")
    except Exception as e:
        logging.critical(f"Failed to process file: {file}; {e}")
        sys.exit(1)


def process_item(key, value, data) -> dict:
    if isinstance(value, str):
        regex_pattern = r"\$\{\{\s*([A-Z0-9_]+)\s*\}\}"

        matches = re.findall(regex_pattern, value)

        for var_name in matches:
            env_value = os.environ.get(var_name)
            if env_value:
                value = re.sub(
                    rf"\$\{{\{{\s*{var_name}\s*\}}\}}", env_value, value
                )
                data[key] = value
            else:
                logging.warning(
                    f"Warning: Environment variable '{var_name}' not found"
                )
    elif isinstance(value, list):
        for v in value:
            process_item(None, v, value)
    elif isinstance(value, dict):
        for k, v in value.items():
            value = process_item(k, v, value)
    return data


def check_for_unsubstituted_variables(data):
    """Recursively checks for unsubstituted variables in a JSON structure."""

    if isinstance(data, dict):
        for key, value in data.items():
            check_for_unsubstituted_variables(value)
    elif isinstance(data, list):
        for item in data:
            check_for_unsubstituted_variables(item)
    elif isinstance(data, str):
        if "${{" in data:  # Change the pattern if needed
            logging.critical(f"Unsubstituted pattern found: {data}")
            sys.exit(1)  # Indicate failure


if __name__ == "__main__":
    print("ENV:", os.environ.items())
    print("SYS ARG", sys.argv)
    logging.basicConfig(level=logging.DEBUG)

    files = os.environ.get("INPUT_FILES", None)
    logging.info(f"INPUT FILES: {files}")
    if files is not None:
        for file in [f.strip() for f in files.split(",")]:
            main(file)
