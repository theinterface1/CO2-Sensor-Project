import unittest


class Tests(unittest.TestCase):

    def test_equal(self):
        self.assertEqual('foo'.upper(), 'FOO')


if __name__ == '__main__':
    unittest.main()
