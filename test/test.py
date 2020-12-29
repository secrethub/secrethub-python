import unittest
import secrethub
import random
import string
import os

TEST_DIR = os.getenv('SECRETHUB_TEST_DIR')

class TestSecretHubClient(unittest.TestCase):

    def test_read_string(self):
        self.assertEqual(secrethub.Client().read_string(TEST_DIR + '/test'), 'foo')

    def test_exists(self):
        self.assertEqual(secrethub.Client().exists(TEST_DIR + '/test'), True)
        self.assertEqual(secrethub.Client().exists(TEST_DIR + '/not-existent'), False)

    def test_write_read_remove(self):
        client = secrethub.Client()
        secret_name = TEST_DIR + "/" + ''.join(random.choice(string.ascii_lowercase) for _ in range(10))
        secret_value = ''.join(random.choice(string.ascii_lowercase) for _ in range(10))
        client.write(secret_name, secret_value)
        self.assertEqual(client.read_string(secret_name), secret_value)
        client.remove(secret_name)

    def test_resolve_env(self):
        os.environ['TEST'] = 'secrethub://'+TEST_DIR+'/test'
        client = secrethub.Client()
        client.export_env(client.resolve_env())
        self.assertEqual(os.environ['TEST'], 'foo')

if __name__ == '__main__':
    unittest.main()
