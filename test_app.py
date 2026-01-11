import unittest
import json
import os
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        # Ensure secret key is set for testing
        os.environ["VERICODE_SECRET_KEY"] = "testsecret"

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Verification Demo', response.data)

    def test_generate_code(self):
        response = self.app.post('/generate',
                                 data=json.dumps({'user_id': 'test@example.com'}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('code', data)
        self.assertTrue(len(data['code']) > 0)

    def test_generate_code_missing_user_id(self):
        response = self.app.post('/generate',
                                 data=json.dumps({}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_validate_code_success(self):
        user_id = 'test@example.com'
        # Generate code first
        gen_response = self.app.post('/generate',
                                     data=json.dumps({'user_id': user_id}),
                                     content_type='application/json')
        code = json.loads(gen_response.data)['code']

        # Validate
        val_response = self.app.post('/validate',
                                     data=json.dumps({'user_id': user_id, 'code': code}),
                                     content_type='application/json')
        self.assertEqual(val_response.status_code, 200)
        self.assertTrue(json.loads(val_response.data)['valid'])

    def test_validate_code_failure(self):
        response = self.app.post('/validate',
                                 data=json.dumps({'user_id': 'test@example.com', 'code': 'wrongcode'}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(json.loads(response.data)['valid'])

    def test_validate_missing_data(self):
        response = self.app.post('/validate',
                                 data=json.dumps({'user_id': 'test@example.com'}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
