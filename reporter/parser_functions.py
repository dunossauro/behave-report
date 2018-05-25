from bs4 import BeautifulSoup as bs


class XmlParser():
    """Class to parse the xml file"""
    def __init__(self, xml_text):
        self.xml_text = self._get_xml(xml_text)

    def _get_xml(self, xml_text) -> object:
        """
            This Function open the xml file and parse it to html.parser

            args:
                file_name: xml file
        """
        file = open(xml_text).read()
        return bs(file, 'html.parser')

    def _get_test_case(self) -> list:
        """
        This Function get all the test cases from the xml files

        args:
        file_name: xml file
        """
        testsuite = self.xml_text.find('testsuite')
        return testsuite.find_all('testcase')

    def _get_failure(self) -> list:
        """
        This Function get all the failures data from the xml file

        args:
        file_name: xml file
        """
        testsuite = self.xml_text.find('testsuite')
        return testsuite.find_all('failure')


    def get_failed_scenarios(self) -> list:
        """
            This Function gets all the failed scenarios from the xml file.

            args:
                xml_text: BeautifulSoup object with html.parser
        """
        testcase = self._get_test_case()

        return [x.attrs for x in testcase if x.attrs['status'] == 'failed']


    def get_passed_scenarios(self) -> list:
        """
        This Function gets all the successful scenarios from the xml file.

        args:
        xml_text: BeautifulSoup object with html.parser
        """
        testcase = self._get_test_case()

        return [x.attrs for x in testcase if x.attrs['status'] == 'passed']


    def get_failed_scenarios(self) -> list:
        """
            This Function gets all the failed scenarios from the xml file.

            args:
                xml_text: BeautifulSoup object with html.parser
        """
        testcase = self._get_test_case()

        return [x.attrs for x in testcase if x.attrs['status'] == 'failed']


    def get_passed_scenarios(self) -> list:
        """
        This Function gets all the successful scenarios from the xml file.

        args:
        xml_text: BeautifulSoup object with html.parser
        """
        testcase = self._get_test_case()

        return [x.attrs for x in testcase if x.attrs['status'] == 'passed']


    def get_failed_scenarios_reason(self):
        failures = self._get_failure()
        return [failed.attrs for failed in failures]


    def get_feature_name(self) -> str:
        """
        This Function gets the feature name from the xml file.

        args:
            xml_text: BeautifulSoup object with html.parser
        """
        testsuite = self.xml_text.find('testsuite')
        return testsuite.attrs['name']
