from re import compile, MULTILINE, DOTALL
from sys import argv
from pandas import DataFrame as df
from bokeh.charts import Donut, show, output_file
from bokeh.embed import file_html
from bokeh.resources import CDN

def head(file):
    """
    Cria o head de do arquivo do parametro
    """
    file.write('<head>\n')
    file.write('<meta charset="utf-8" />\n')
    file.write('<title>Behave Report</title>\n')
    file.write('</head>\n')
    file.write('<body>\n')
    file.write('<div align="center">\n')
    file.write('<h1>BEHAVE REPORT</h1>\n')

remove_scenarios = compile(
    "@scenario.begin(.*?)@scenario.end", MULTILINE | DOTALL)
scenarios = compile("Cenário: .*|Contexto: .*")
steps = compile("\s+(Então|Quando|Dado)(.*?) ... (failed|passed|skipped) in (.*)")

xml = open(argv[1]).read()
html = open(argv[2], 'w')

a = remove_scenarios.findall(xml)[0].lstrip()
b = scenarios.findall(a)[0]
c = steps.findall(a)

g = df(c, columns=['step', 'text', 'state', 'time'])


h = Donut(g, label='state')

head(html)
html.write(file_html(h, CDN))
html.write("<h4>{}</h4>".format(b))
html.write(g.to_html())
