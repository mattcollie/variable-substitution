import json
import sys

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
            print(f"Unsubstituted pattern found: {data}")
            sys.exit(1)  # Indicate failure

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_json_substitution.py <json_file>")
        sys.exit(1)

    json_file = sys.argv[1]
    with open(json_file, 'r') as f:
        data = json.load(f)

    check_for_unsubstituted_variables(data)
    print("All variables substituted successfully!")
