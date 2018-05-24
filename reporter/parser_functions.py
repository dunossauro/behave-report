from bs4 import BeautifulSoup as bs

def get_xml(file_name):
    file = open(file_name).read()
    return bs(file, 'html.parser')


def get_failed_scenarios(xml_text):
    testsuite = xml_text.find('testsuite')
    testcase = testsuite.find_all('testcase')

    return [x.attrs['name'] for x in testcase if x.attrs['status'] == 'failed']
