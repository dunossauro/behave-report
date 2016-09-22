from re import compile, MULTILINE, DOTALL
from collections import Counter
from bokeh.plotting import figure
from bokeh.embed import file_html
from bokeh.resources import CDN
from numpy import pi

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

xml = open('TESTS-lista_global.xml').read()
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
        color = colors['failed']
        status = 'FAILED'

    elif dic['skipped'] > 0:
        color = colors['skipped']
        status = 'SKIPPED'
    else:
        color = color['passed']
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

    percents = [dic['skipped']/100, dic['passed']/100, dic['failed']/100]
    starts = [p*2*pi for p in percents[:-1]]
    ends = [p*2*pi for p in percents[1:]]

    colors_ = ["red", "green", "blue"]

    p = figure(x_range=(-1,1), y_range=(-1,1))

    p.wedge(x=0, y=0, radius=1, start_angle=starts, end_angle=ends, color=colors_)


html.write(file_html(p, CDN))
html.close()
