# -*- coding: utf-8 -*

from sys import argv
# from os import listdir
from re import compile as r_compile
from re import MULTILINE, DOTALL
from bokeh.charts import Donut
from bokeh.embed import components
from bokeh.resources import INLINE
from pandas import DataFrame as df
from pandas import concat
from jinja2 import FileSystemLoader, Environment
# from pages import out_index

# Regex
REMOVE_SCENARIOS = r_compile(
    r"^@scenario.begin(.*?)@scenario.end$", MULTILINE | DOTALL)

# --- get scenarios
SCENARIOS = r_compile(r"Cen[á|a]rio: .*|Contexto: .*")

# --- get steps
step_words = r'(E\s|Ent[ã|a]o|Quando|Dad[o|a|as|os]|Mas)'
step_state = r'(failed|passed|skipped)'

STEPS = r_compile(r"\s+{s_w}(.*?) ... {s_s} in (.*)".format(
                   s_w=step_words,
                   s_s=step_state))

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
    temp_path = FileSystemLoader(searchpath="./templates")

    j_env = Environment(loader=temp_path)

    template = j_env.get_template("./report.html")

    tup = mount_graph()

    vars = {"boke_js": INLINE.render_js(),
            "boke_css": INLINE.render_css(),
            "feature": NAME.findall(XML)[0],
            "failed": ERRORS.findall(XML)[0],
            "skipped": SKIPPED.findall(XML)[0],
            "FILO": FILO,
            "errors": ERROR_DESC.findall(XML),
            "title": tup[0],
            "graph": tup[1]}

    with open('{}.html'.format(argv[1][:-4]), 'w') as rp:
        rp.writelines(template.render(vars))


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
    try:
        XML = open(argv[1]).read()
        parse_xml(XML)
        mount_page()
    except IndexError:
        print("Use:\nreporter.py <behave_file.xml>")
