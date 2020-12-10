import unittest
import secrethub

class TestSecretHubClient(unittest.TestCase):

    def test_read_string(self):
        self.assertEqual(secrethub.Client().read_string('secrethub/xgo/python/test/test'), 'foo')

if __name__ == '__main__':
    unittest.main()