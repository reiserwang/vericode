# Gemini Code Generation Instructions

## Objective

Generate a reusable Python module for creating and validating time-bound verification codes. The module should be self-contained, well-documented, and include example usage.

## Project Description

The goal is to create a system that generates short, user-friendly verification codes (like OTPs). These codes are deterministically generated from a user's identifier and the current time, making them automatically expire after a configured period. This allows for stateless, time-sensitive validation, which is ideal for scenarios where you want to avoid storing the code in a database.

### Key Features:

1.  **Configurable Code Patterns**: The generated codes should be customizable in terms of:
    *   `length`: The number of characters in the code (default: 6).
    *   `charset`: The characters to use, with options for:
        *   Numeric digits (0-9).
        *   Uppercase letters (A-Z).
        *   Lowercase letters (a-z).
    *   The default should be a 6-digit numeric code.

2.  **Time-Bound Generation**: The code generation is based on a hash of the `user_id`, a `SECRET_KEY`, and a time-based salt derived from the current time, quantized by a configurable `period`. This makes the codes inherently time-sensitive.

3.  **Stateless, Time-Aware Validation**: The module must provide a function to validate a given code against a `user_id` and a `period`. The validation will check against both the current and the previous time window to account for clock drift or delays.



## Developer Setup and Execution using `uv`

This section describes how to set up a virtual environment and run the generated Python scripts using `uv`, a fast Python package installer and resolver. As this project only uses the standard library, no external packages need to be installed.

### 1. Install `uv`

If you don't have `uv` installed, follow the official installation instructions. For example, on macOS and Linux:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Create and Activate a Virtual Environment

Navigate to the project directory, then create and activate a virtual environment.

```bash
# Create the virtual environment in a .venv directory
uv venv

# Activate the environment (on macOS/Linux)
source .venv/bin/activate
```

### 3. Run the Code

Once the environment is activated, you can run the example script and the tests.

```bash
# Run the example usage script
python verification_code_generator.py

# Run the test suite
python test_verification_code_generator.py
```