import unittest
from reporter.parser_functions import (get_xml, get_failed_scenarios)
from bs4 import BeautifulSoup as bs


class ParserFunctions(unittest.TestCase):

    def test_get_xml_file_expected_to_be_a_bs_instance(self):
        result = get_xml('tests/teste.xml')
        self.assertIsInstance(result, bs)


    def test_get_failed_scenarios_expected_to_be_a_list_of_strings(self):
        xml = get_xml('tests/teste.xml')
        result = get_failed_scenarios(xml)
        self.assertIsInstance(result, list)
        for item in result:
            self.assertIsInstance(item, str)
