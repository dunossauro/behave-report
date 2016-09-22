from re import compile, MULTILINE, DOTALL
from collections import Counter
colors = {
    'failed': 'red',
    'passed': 'green',
    'skipped': 'blue',
}


def head(file):
    file.write('<head>')
    file.write('<meta charset="utf-8" />')
    file.write('</head>')
    file.write('<body>')

# Baseic regex
remove_scenarios = compile(
    "@scenario.begin(.*?)@scenario.end", MULTILINE | DOTALL)
scenarios = compile("Cenário: .*|Contexto: .*")
steps = compile("\s+(.*?) ... (failed|passed|skipped) in (.*)")

xml = open('TESTS-teste.xml').read()
html = open('out.html', 'w')

head(html)

for test in remove_scenarios.findall(xml):
    cen = scenarios.findall(test)
    html.write('<h4>' + "".join(cen) + '</h4>')

    out = steps.findall(test)
    for x in out:
        topics = x[0].split()
        text = " ".join(topics[1:])

        html.write(
            '<b>{}</b> {}<font color="{}"> {}</font> in {}'.format(
                topics[0],
                text,
                colors[x[1]],
                x[1],
                x[2]))
        html.write('<br>')

    results = len(out)
    dic = Counter([x[1] for x in out])
    if dic['failed'] != 0:
        color = 'red'
        status = 'FAILED'
    else:
        color = 'green'
        status = 'PASSED'

    if dic['passed'] == results:
        html.write('<br>\
        <b>\
        <font color="{}">{}</font>\
        </b>'.format(color, status))
    else:
        html.write('<br>\
        <b>\
        <font color="{}">{} {} steps:</font>\
        </b>'.format(color, status, results))
        for x in dic:
            html.write("<br> {}: {}".format(dic[x], x))

html.close()
