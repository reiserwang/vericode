"""A module for generating and validating stateless, time-bound verification codes."""

import hashlib
import hmac
import string
import time
from typing import Optional

# For production use, this should be loaded securely, e.g., from an environment
# variable or a secrets management system. It should not be hardcoded.
import os
import json

SECRET_KEY = os.environ.get("VERICODE_SECRET_KEY")
if not SECRET_KEY:
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
            SECRET_KEY = config.get("VERICODE_SECRET_KEY")
    except FileNotFoundError:
        pass # Handled by the next check

if not SECRET_KEY:
    raise ValueError("VERICODE_SECRET_KEY not set in environment or config.json.")

def _generate_code_for_time_bucket(
    user_id: str,
    time_bucket: int,
    length: int,
    charset: str,
    counter: Optional[int] = None,
) -> str:
    """Helper function to generate a code for a specific time bucket."""
    message = f"{user_id}:{time_bucket}:{counter}:{SECRET_KEY}"
    h = hashlib.sha256(message.encode("utf-8")).digest()
    num = int.from_bytes(h, "big")

    code = []
    for _ in range(length):
        index = num % len(charset)
        code.append(charset[index])
        num >>= 3

    return "".join(code)

def generate_code(
    user_id: str,
    period: int = 300,
    length: int = 6,
    use_digits: bool = True,
    use_uppercase: bool = False,
    use_lowercase: bool = False,
    counter: Optional[int] = None,
) -> str:
    """Generates a deterministic, time-bound verification code.

    The code is generated based on the user_id, a secret key, and the current
    time, quantized by the period. This makes it reproducible and automatically
    expiring.

    Args:
        user_id: The user's unique identifier (e.g., email, phone number).
        period: The validity period of the code in seconds (default: 300s).
        length: The desired length of the verification code.
        use_digits: Whether to include numeric digits in the character set.
        use_uppercase: Whether to include uppercase letters.
        use_lowercase: Whether to include lowercase letters.

    Returns:
        The generated code.

    Raises:
        ValueError: If no character set is selected.
    """

    charset = ""
    if use_digits:
        charset += string.digits
    if use_uppercase:
        charset += string.ascii_uppercase
    if use_lowercase:
        charset += string.ascii_lowercase

    if not charset:
        raise ValueError("At least one character set must be selected.")

    current_time_bucket = int(time.time() / period)
    return _generate_code_for_time_bucket(
        user_id, current_time_bucket, length, charset, counter
    )

def validate_code(
    code: str,
    user_id: str,
    period: int = 300,
    use_digits: bool = True,
    use_uppercase: bool = False,
    use_lowercase: bool = False,
    counter: Optional[int] = None,
) -> bool:
    """Validates a time-bound verification code.

    It validates the code against the current and previous time periods to
    account for clock drift or delays.

    Args:
        code: The verification code to validate.
        user_id: The user's unique identifier.
        period: The validity period used during generation.
        use_digits: Must match the setting used for code generation.
        use_uppercase: Must match the setting used for code generation.
        use_lowercase: Must match the setting used for code generation.

    Returns:
        True if the code is valid, False otherwise.
    """

    if not code:
        return False

    charset = ""
    if use_digits:
        charset += string.digits
    if use_uppercase:
        charset += string.ascii_uppercase
    if use_lowercase:
        charset += string.ascii_lowercase

    if not charset:
        return False # Or raise ValueError, consistent with generate_code

    current_time_bucket = int(time.time() / period)
    previous_time_bucket = current_time_bucket - 1

    # Check current time bucket
    expected_code_current = _generate_code_for_time_bucket(
        user_id, current_time_bucket, len(code), charset, counter
    )
    if hmac.compare_digest(code, expected_code_current):
        return True

    # Check previous time bucket
    expected_code_previous = _generate_code_for_time_bucket(
        user_id, previous_time_bucket, len(code), charset, counter
    )
    if hmac.compare_digest(code, expected_code_previous):
        return True

    return False

if __name__ == "__main__":
    while True:
        print("\n--- Verification Code Generator ---")
        print("1. Generate a new verification code")
        print("2. Validate a verification code")
        print("3. Exit")
        choice = input("Choose an option (1/2/3): ")

        if choice == '1':
            user_id = input("Enter User ID: ")
            length_str = input("Enter code length (default: 6): ")
            length = int(length_str) if length_str.isdigit() else 6

            use_digits = input("Use digits (0-9)? (y/n, default: y): ").lower() != 'n'
            use_uppercase = input("Use uppercase (A-Z)? (y/n, default: n): ").lower() == 'y'
            use_lowercase = input("Use lowercase (a-z)? (y/n, default: n): ").lower() == 'y'
            counter_str = input("Enter optional counter (integer, leave blank for none): ")
            counter = int(counter_str) if counter_str.isdigit() else None

            try:
                code = generate_code(
                    user_id,
                    length=length,
                    use_digits=use_digits,
                    use_uppercase=use_uppercase,
                    use_lowercase=use_lowercase,
                    counter=counter
                )
                print(f"\nGenerated Code: {code}")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == '2':
            user_id = input("Enter User ID: ")
            code = input("Enter verification code: ")
            
            # We need to ask for the original code generation parameters
            # to ensure validation works correctly.
            use_digits = input("Was it generated with digits? (y/n, default: y): ").lower() != 'n'
            use_uppercase = input("Was it generated with uppercase? (y/n, default: n): ").lower() == 'y'
            use_lowercase = input("Was it generated with lowercase? (y/n, default: n): ").lower() == 'y'
            counter_str = input("Was a counter used? (integer, leave blank for none): ")
            counter = int(counter_str) if counter_str.isdigit() else None

            is_valid = validate_code(
                code,
                user_id,
                use_digits=use_digits,
                use_uppercase=use_uppercase,
                use_lowercase=use_lowercase,
                counter=counter
            )
            if is_valid:
                print("\nResult: Code is VALID.")
            else:
                print("\nResult: Code is INVALID.")

        elif choice == '3':
            print("Exiting.")
            break

        else:
            print("Invalid choice. Please try again.")