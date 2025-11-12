import unittest

from src.roman_parser import *

class TestRommanGrammar(unittest.TestCase):
    def _check_analyze(self, input_string, int_value, valid):
        try:
            result = parser.parse(input_string)
            if not valid:
                assert(result["valid"] == valid)
            else:
                assert(result["valid"] == valid and result["val"] == int_value)
        except:
            assert(not valid)

    def test_cases_1(self):
        self._check_analyze("XX", 20, True)

    def test_cases_2(self):
        self._check_analyze("IX", 9, True)

    def test_cases_3(self):
        self._check_analyze("XII", 12, True)

    def test_cases_4(self):
        self._check_analyze("XIIII", 13, False)


if __name__ == '__main__':
    unittest.main()
