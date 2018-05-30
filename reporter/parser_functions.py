from collections import ChainMap
from bs4 import BeautifulSoup as bs

def xml_parser(xml_text, status:str):
    """
    This Function scrapps all data from the xml file

    args:
        xml_text: BeautifulSoup object with html.parser
        status: failed or passed (TODO: implement skipped)

    returns:
        testsuite.attrs: feature data
        scenarios: scenarios data (failed or passed)
    """
    xml_text = bs(open(xml_text).read(), 'html.parser')
    testsuite = xml_text.find('testsuite')
    testcase = testsuite.find_all('testcase')
    failures = testsuite.find_all('failure')

    scenarios = [x.attrs for x in testcase if x.attrs['status'] == status]
    if status == 'failed':
        return testsuite.attrs, [dict(ChainMap(scenarios, failure.attrs))
                for scenarios, failure in zip(scenarios, failures)]
    return testsuite.attrs, scenarios
