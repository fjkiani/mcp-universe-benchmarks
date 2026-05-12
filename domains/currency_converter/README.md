# currency_converter Domain

This domain contains benchmark tasks for currency_converter.

## Structure

- `config.yaml` - Domain benchmark configuration
- `tasks/` - Individual task definition files
- `evaluators/` - Evaluation functions
- `README.md` - This file

## Tasks

Total tasks: 1

## Evaluators

Evaluation functions are located in `evaluators/functions.py`.

## Usage

```bash
# Validate this domain
alignerr validate --domain currency_converter

# Validate with specific model
alignerr validate --domain currency_converter --model openai/gpt-4o
```

## Development

Add new tasks by creating JSON files in the `tasks/` directory.
Update evaluation functions in `evaluators/functions.py`.
