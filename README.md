# Verification Code Generator

This Python module provides a robust and stateless solution for generating and validating verification codes (like OTPs). The codes are deterministically generated based on a user identifier and a time-based component, allowing for validation without needing to store the generated code in a database.

## Features

*   **Configurable Code Patterns**: Customize code length and character sets (digits, uppercase, lowercase).
*   **Deterministic Generation**: Codes are reproducible based on `user_id`, a time-based salt, and a `SECRET_KEY`.
*   **Stateless Validation**: Validate codes without storing them, by regenerating the expected code and comparing it.
*   **Console UI**: An interactive command-line interface for easy generation and validation.

## Algorithm

The core of this module relies on a deterministic process to generate codes:

1.  **Time-Based Salt**: The current time is divided by a `period` (default 300 seconds) to create a time bucket. This time bucket acts as a dynamic salt, ensuring that codes change over time for the same user ID.
2.  **Hashing**: The `user_id`, the calculated time bucket, and a `SECRET_KEY` are concatenated and then hashed using SHA-256. This ensures the input is securely and consistently transformed.
3.  **Code Generation**: The hexadecimal digest of the hash is converted into a large integer. Characters for the verification code are then picked from the defined `charset` by repeatedly taking the modulo of this integer with the length of the `charset`. After each character selection, the integer is bit-shifted (`>> 3`) to use different parts of the hash for subsequent characters, improving character distribution.
4.  **Validation**: To validate a code, the system regenerates the expected code using the provided `user_id`, the current time bucket, and the same generation parameters. It also regenerates a code for the *previous* time bucket to account for minor clock drifts or delays in validation. The provided code is then compared against these regenerated codes using `hmac.compare_digest` for constant-time comparison, mitigating timing attacks.

## Usage

### Interactive Console UI

To use the interactive console, run the `verification_code_generator.py` script directly:

```bash
python verification_code_generator.py
```

Follow the prompts to generate a new code or validate an existing one.

### Programmatic Usage

You can also import and use the `generate_code` and `validate_code` functions in your Python applications:

```python
from verification_code_generator import generate_code, validate_code

# Generate a default 6-digit numeric code
user_id = "test@example.com"
code = generate_code(user_id)
print(f"Generated Code: {code}")

# Validate the code
is_valid = validate_code(code, user_id)
print(f"Is valid: {is_valid}")

# Generate an 8-character alphanumeric code
alphanumeric_code = generate_code(
    "another_user@example.com",
    length=8,
    use_digits=True,
    use_uppercase=True,
    use_lowercase=True
)
print(f"Alphanumeric Code: {alphanumeric_code}")

# Validate the alphanumeric code
is_alphanumeric_valid = validate_code(
    alphanumeric_code,
    "another_user@example.com",
    length=8,
    use_digits=True,
    use_uppercase=True,
    use_lowercase=True
)
print(f"Is alphanumeric valid: {is_alphanumeric_valid}")

# Example of an expired code (using a very short period for demonstration)
# In a real application, the period would be much longer (e.g., 300 seconds).
import time
short_period_code = generate_code("time_sensitive@example.com", period=1)
print(f"Short period code: {short_period_code}")
time.sleep(2) # Wait for the code to expire (pass two periods)
is_expired = validate_code("time_sensitive@example.com", short_period_code, period=1)
print(f"Is short period code expired: {is_expired}")
```

#### `generate_code` parameters:

*   `user_id` (str): The unique identifier for the user.
*   `period` (int, optional): The validity period of the code in seconds. Defaults to 300 (5 minutes). This value determines the granularity of the time-based salt.
*   `length` (int, optional): The desired length of the code. Defaults to 6.
*   `use_digits` (bool, optional): Include digits (0-9). Defaults to `True`.
*   `use_uppercase` (bool, optional): Include uppercase letters (A-Z). Defaults to `False`.
*   `use_lowercase` (bool, optional): Include lowercase letters (a-z). Defaults to `False`.

#### `validate_code` parameters:

*   `code` (str): The verification code to validate.
*   `user_id` (str): The user's unique identifier.
*   `period` (int, optional): The validity period used during generation. Must match the value used when the code was generated. Defaults to 300.
*   `use_digits` (bool, optional): Must match the setting used for code generation. Defaults to `True`.
*   `use_uppercase` (bool, optional): Must match the setting used for code generation. Defaults to `False`.
*   `use_lowercase` (bool, optional): Must match the setting used for code generation. Defaults to `False`.

## Code Quality

*   **Docstrings**: Clear and concise docstrings for the module and each function.
*   **Type Hinting**: Python's type hints are used for all function signatures.
*   **Security**: Uses `hmac.compare_digest` for constant-time comparison to prevent timing attacks.
*   **Standard Libraries**: Only uses Python standard libraries (`hashlib`, `hmac`, `string`, `time`).
