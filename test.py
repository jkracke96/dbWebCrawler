import unittest
from stringConverter import convertString, convertDate


class TestStringConverter(unittest.TestCase):
    def test_convert_string(self):
        """
        test convert string function
        """
        from extractData import findBlock
        to_replace = "(Halt entfaellt)"
        result = convertString(to_replace)
        self.assertEqual("", result)

    def test_convert_date(self):
        """
        test convert date function
        """
        from extractData import findBlock
        to_replace = "0024002001"
        result = convertDate(to_replace)
        self.assertEqual("01.02.24", result)


if __name__ == '__main__':
    unittest.main()
