from re import compile, MULTILINE, DOTALL

remove_scenarios = compile("@scenario.begin(.*?)@scenario.end", MULTILINE | DOTALL)
scenarios = compile("Cenário: .*")
steps = compile("\s+(.*?) ... (failed|passed|skipped) in (.*)")

xml = open('TESTS-teste.xml').read()

a = "".join(remove_scenarios.findall(xml))

out = steps.findall(a)

for x in out: print(x)
