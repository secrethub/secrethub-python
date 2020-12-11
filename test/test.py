import unittest
import secrethub
import random
import string

class TestSecretHubClient(unittest.TestCase):

    def test_read_string(self):
        self.assertEqual(secrethub.Client().read_string('secrethub/xgo/python/test/test'), 'foo')

    def test_exists(self):
        self.assertEqual(secrethub.Client().exists('secrethub/xgo/python/test/test'), True)
        self.assertEqual(secrethub.Client().exists('secrethub/xgo/python/test/not-existent'), False)

    def test_write_read_remove(self):
        client = secrethub.Client()
        secret_name = "secrethub/xgo/python/test/" + ''.join(random.choice(string.ascii_lowercase) for _ in range(10))
        secret_value = ''.join(random.choice(string.ascii_lowercase) for _ in range(10))
        client.write(secret_name, secret_value)
        self.assertEqual(client.read_string(secret_name), secret_value)
        client.remove(secret_name)

if __name__ == '__main__':
    unittest.main()
