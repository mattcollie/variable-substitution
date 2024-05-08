import json
import sys
import logging


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
    if len(sys.argv) != 2:
        logging.critical("Usage: python test_json_substitution.py <json_file>")
        sys.exit(1)

    files = sys.argv[1]
    for file in [f.strip() for f in files.split(',')]:
        with open(file, 'r') as f:
            data = json.load(f)

        check_for_unsubstituted_variables(data)
        logging.info(f"All variables substituted successfully for: {file}!")
