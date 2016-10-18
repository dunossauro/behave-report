# -*- coding: utf-8 -*

from sys import argv
from os import listdir
from re import compile as r_compile
from re import MULTILINE, DOTALL
from bokeh.charts import Donut
from bokeh.embed import components
from bokeh.resources import INLINE
from pandas import DataFrame as df
from pandas import concat
from pages import out_index
import jinja2

# Regex
REMOVE_SCENARIOS = r_compile(
    r"^@scenario.begin(.*?)@scenario.end$", MULTILINE | DOTALL)
# --- get scenarios
SCENARIOS = r_compile(r"Cen[á|a]rio: .*|Contexto: .*")
# --- get steps
STEPS = r_compile(
    r"\s+(E\s|Ent[ã|a]o|Quando|Dad[o|a|as|os]|Mas)(.*?) ... (failed|passed|skipped) in (.*)")
# --- get data
ERRORS = r_compile(r'errors="(\d)"')
SKIPPED = r_compile(r'skipped="(\d)"')
NAME = r_compile(r'<testcase classname=".*?\.(.*?)"')
ERROR_DESC = r_compile(r'CDATA\[(.*)]]>.*</error>', MULTILINE | DOTALL)

L_DFS = []  # ----- Lista dos dataframes para compilação

FILO = []   # ----- Fila para o html


def mount_page():
    """
    monta uma pagina diferente para cada report chamando os templates do jinja
    """
    templateLoader = jinja2.FileSystemLoader(searchpath="./templates")

    templateEnv = jinja2.Environment(loader=templateLoader)

    template = templateEnv.get_template("./report.html")

    tup = mount_graph()

    templateVars = {"boke_js": INLINE.render_js(),
                    "boke_css": INLINE.render_css(),
                    "feature": NAME.findall(XML)[0],
                    "failed": ERRORS.findall(XML)[0],
                    "skipped": SKIPPED.findall(XML)[0],
                    "FILO": FILO,
                    "errors": ERROR_DESC.findall(XML),
                    "title": tup[0],
                    "graph": tup[1]}

    with open('{}.html'.format(argv[1][:-4]), 'w') as rp:
        rp.writelines(template.render(templateVars))


def mount_graph():
    """
    Função que monta o gráfico usando os dataframes
    """
    all_df = concat(L_DFS)
    graph = Donut(all_df, label='state')
    return components(graph, INLINE)

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

        FILO.append(
            "<h4>{}</h4>".format("".join(SCENARIOS.findall(splited_text))))
        FILO.append(text_df.to_html(classes="table"))

if __name__ == '__main__':
    XML = open(argv[1]).read()
    parse_xml(XML)
    mount_page()

    pages = [x[:-5] for x in listdir('.') if x[-4:] == 'html']
    out_index(pages)
