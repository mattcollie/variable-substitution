[![Integration Test](https://github.com/mattcollie/variable-substitution/actions/workflows/integration.yml/badge.svg)](https://github.com/mattcollie/variable-substitution/actions/workflows/integration.yml)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/mattcollie/variable-substitution/blob/main/LICENSE)

# variable-substitution
A Github Action for substituting variables within JSON files using env variables.

---

## Inputs

- `files` (required): A comma-separated list of JSON files to process.
    File paths are relative to the workspace root.

## Outputs

This action does not have any outputs.

---

## Usage Example

### Workflow that uses the action
```yaml
jobs:
  my_job:
    env:
      ENVIRONMENT: production
      API_ENDPOINT: https://api.example.com
    
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Substitute Variables
        uses: mattcollie/variable-substitution@v1
        with:
          files: config.json
```

### Original `config.json`:
```json
{
  "api_url": "${{ API_ENDPOINT }}",
  "environment": "${{ ENVIRONMENT }}",
  "description": "Configuration for env: ${{ ENVIRONMENT }}"
}
```

### After Substitution:

(Assuming your workflow defines the necessary secrets and environment variables)
```json
{
  "api_url": "https://api.example.com",
  "environment": "production",
  "description": "Configuration for env: production"
}
```
