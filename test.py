import unittest
from unittest.mock import Mock
from stringConverter import convertString, convertDate
from pymongo_connect import MongoDB


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


"""class TestPyMongoConnect(unittest.TestCase):
    def test_get_db(self):
        client = {
            "dbWebCrawler": {
                "cancellations": "test"
            }
        }
        mongo = MongoDB()
        result = mongo.get_db(client=client)
        self.assertEqual("test", result)"""


if __name__ == '__main__':
    unittest.main()
