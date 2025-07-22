"""Tests for the verification_code_generator module.""" 

import time 
import unittest 
from unittest.mock import patch 

from verification_code_generator import generate_code, validate_code 

class TestVerificationCodeGenerator(unittest.TestCase): 

    def test_generate_code_default(self): 
        """Test default code generation (6-digit numeric).""" 
        code = generate_code("test@example.com") 
        self.assertEqual(len(code), 6) 
        self.assertTrue(code.isdigit()) 

    def test_generate_code_custom_length(self): 
        """Test code generation with a custom length.""" 
        code = generate_code("test@example.com", length=8) 
        self.assertEqual(len(code), 8) 

    def test_generate_code_alphanumeric(self): 
        """Test alphanumeric code generation.""" 
        code = generate_code( 
            "test@example.com", 
            length=12, 
            use_digits=True, 
            use_uppercase=True, 
            use_lowercase=True, 
        ) 
        self.assertTrue(code.isalnum()) 

    def test_generate_code_no_charset(self): 
        """Test that generation fails if no character set is selected.""" 
        with self.assertRaises(ValueError): 
            generate_code( 
                "test@example.com", 
                use_digits=False, 
                use_uppercase=False, 
                use_lowercase=False, 
            ) 

    def test_validate_code_success(self): 
        """Test successful validation within the same time period.""" 
        user_id = "validate@example.com" 
        code = generate_code(user_id) 
        self.assertTrue(validate_code(code, user_id)) 

    def test_validate_code_failure_wrong_code(self): 
        """Test validation failure with an incorrect code.""" 
        user_id = "validate@example.com" 
        generate_code(user_id) # Ensure time bucket is used 
        self.assertFalse(validate_code("000000", user_id)) 

    def test_validate_code_failure_wrong_config(self): 
        """Test validation failure with mismatched generation config.""" 
        user_id = "validate@example.com" 
        code = generate_code(user_id, use_uppercase=True) 
        self.assertFalse(validate_code(code, user_id, use_uppercase=False)) 

     

if __name__ == "__main__": 
    unittest.main()
