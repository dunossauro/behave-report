from sys import argv
from re import compile as r_compile
from re import MULTILINE, DOTALL
from bokeh.charts import Donut
from bokeh.embed import file_html
from bokeh.resources import CDN
from pandas import DataFrame as df
from pandas import concat

#Regex
REMOVE_SCENARIOS = r_compile(
    r"@scenario.begin(.*?)@scenario.end", MULTILINE | DOTALL)
R_SCENARIOS = r_compile(r"Cenário: .*|Contexto: .*")
R_STEPS = r_compile(
    r"\s+(Então|Quando|Dado)(.*?) ... (failed|passed|skipped) in (.*)")

L_DFS = [] # ----- Lista dos dataframes para compilação

FILO = []   # ----- Fila para o html

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


def mount_graph(file):
    """
    Função que monta o gráfico usando os dataframes
    """
    all_df = concat(L_DFS)
    graph = Donut(all_df, label='state')
    file.write(file_html(graph, CDN))


def mount_page(file):
    """
    Esgota a fila enviado para o html
    """
    for saida in FILO:
        file.write(saida)


def todo(file):
    """
    função que precisa ser modificada
    pois faz tudo
    """
    for text in REMOVE_SCENARIOS.findall(file):
        splited_text = text.lstrip()

        steps = R_STEPS.findall(splited_text)

        text_df = df(steps, columns=['step', 'text', 'state', 'time'])
        L_DFS.append(text_df)

        FILO.append("<h4>{}</h4>".format("".join(R_SCENARIOS.findall(splited_text))))
        FILO.append(text_df.to_html())

if __name__ == '__main__':
    XML = open(argv[1]).read()
    HTML = open(argv[2], 'w')

    head(HTML)
    todo(XML)
    mount_graph(HTML)
    mount_page(HTML)

    HTML.close()
