from unittest import TestLoader, runner
from click import group, argument


@group()
def cmds():
    pass


@cmds.command(help='parser behave xml file')
@argument('xml',)
@argument('html')
def parse(xml, html):
    pass


@cmds.command()
def unittests():
    loader = TestLoader()
    tests = loader.discover('tests/')
    testRunner = runner.TextTestRunner()
    testRunner.run(tests)


cmds()
