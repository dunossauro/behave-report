from reporter.parser_functions import xml_parser
from os import listdir
from os.path import isfile, join

def list_features(path):
    return [file for file in listdir(path) if isfile(join(path, file))]

def create_table_titles(titles:list):
    return  ' | *' + '* | *'.join(titles) + '* | '

def create_feature_line():
    for x in open('reporter/features'):
        import ipdb; ipdb.set_trace()
        feature, scenarios_passed = xml_parser('reporter/features{}.xml', 'passed')
        _, scenarios_failed = xml_parser('reporter/features{}.xml', 'failed')
    return False
