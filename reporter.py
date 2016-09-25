from sys import argv
from re import compile as r_compile
from re import MULTILINE, DOTALL
from bokeh.charts import Donut
from bokeh.embed import components
from bokeh.resources import INLINE
from pandas import DataFrame as df
from pandas import concat

#Regex
REMOVE_SCENARIOS = r_compile(
    r"@scenario.begin(.*?)@scenario.end", MULTILINE | DOTALL)
SCENARIOS = r_compile(r"Cenário: .*|Contexto: .*")
STEPS = r_compile(
    r"\s+(Então|Quando|Dado)(.*?) ... (failed|passed|skipped) in (.*)")

L_DFS = [] # ----- Lista dos dataframes para compilação

FILO = []   # ----- Fila para o html

def head(file, tup):
    """
    Cria o head de do arquivo do parametro
    """
    style_table = """
    <style>
        table {
            border-collapse: collapse;
            width: 100%;
        }

        th, td {
            text-align: left;
            padding: 8px;
            }

        tr:nth-child(even){background-color: #f2f2f2}
    </style>
    """
    file.write('<!DOCTYPE html>\n')
    file.write('<html>\n')
    file.write('<head>\n')
    file.write('\t<meta charset="utf-8" />\n')
    file.write('\t<title>Behave Report</title>\n')
    file.write(INLINE.render_js())
    file.write(INLINE.render_css())
    file.write('{}\n'.format(style_table))
    file.write('\t{}\n'.format(tup[0]))
    file.write('</head>\n')
    file.write('<body>\n')
    file.write('\t<div align="center">\n')
    file.write('\t\t<h1>BEHAVE REPORT</h1>\n')
    file.write('\t{}\n'.format(tup[1]))
    file.write('\t</div>\n')


def mount_graph():
    """
    Função que monta o gráfico usando os dataframes
    """
    all_df = concat(L_DFS)
    graph = Donut(all_df, label='state')
    return components(graph, INLINE)

def mount_page(file, component):
    """
    Esgota a fila enviado para o html
    """
    head(HTML, component)
    for saida in FILO:
        file.write(saida)
    file.write('</html>')
    file.close()

def parse_xml(file):
    """
    Função que itera a regex, cria data frames
    e gera a fila de htmls para o arquivo
    """
    for text in REMOVE_SCENARIOS.findall(file):
        splited_text = text.lstrip()

        steps = STEPS.findall(splited_text)

        text_df = df(steps, columns=['step', 'text', 'state', 'time'])
        L_DFS.append(text_df)

        FILO.append("<h4>{}</h4>".format("".join(SCENARIOS.findall(splited_text))))
        FILO.append(text_df.to_html())

if __name__ == '__main__':
    XML = open(argv[1]).read()
    HTML = open(argv[2], 'w')

    parse_xml(XML)
    BCOMPS = mount_graph()
    mount_page(HTML, BCOMPS)
