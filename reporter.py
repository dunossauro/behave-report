from sys import argv
from re import compile as r_compile
from re import MULTILINE, DOTALL
from bokeh.charts import Donut
from bokeh.embed import components
from bokeh.resources import INLINE
from pandas import DataFrame as df
from pandas import concat

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


def head(file, tup):
    """
    Cria o head do arquivo usando o parametro
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
    # ---- Style
    file.write(INLINE.render_js())
    file.write(INLINE.render_css())
    # ---- bootstrap
    file.write('<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"\
                rel="stylesheet"\
                integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u"\
                crossorigin="anonymous">')

    file.write('<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js">\
                </script>')
    file.write('<script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js">\
                </script>')

    file.write('{}\n'.format(style_table))
    file.write('\t{}\n'.format(tup[0]))
    file.write('</head>\n')
    file.write('<body>\n')
    file.write('\t<div align="center">\n')
    file.write('\t\t<h1>BEHAVE REPORT</h1>\n')
    file.write('\t{}\n'.format(tup[1]))

    # ---- Parse informations
    file.write('\t<h3>Feature: {}</h3><br>\n'.format(
        NAME.findall(XML)[0]))
    file.write('\t</div>\n')
    file.write('\tScenarios failed: {}<br>\n'.format(
        ERRORS.findall(XML)[0]))
    file.write('\tScenarios skipped: {}<br>\n'.format(
        SKIPPED.findall(XML)[0]))


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
    file.write('<br>' * 2)
    # --- Write error in code font
    file.write("""
  <div class="panel panel-default">
    <div class="panel-heading">
      <h4 class="panel-title">
        <a data-toggle="collapse" data-parent="#accordion" href="#collapse1">
        ERRORS</a>
      </h4>
    </div>
    <div id="collapse1" class="panel-collapse collapse in">
    """.format('ERRORS'))
    for error in ERROR_DESC.findall(XML):
        file.write(error.replace('\n', '<br>'))
    file.write('</div>\n</div>\n</html>')
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

        FILO.append(
            "<h4>{}</h4>".format("".join(SCENARIOS.findall(splited_text))))
        FILO.append(text_df.to_html(classes="table"))

if __name__ == '__main__':
    XML = open(argv[1]).read()
    HTML = open(argv[2], 'w')

    parse_xml(XML)
    COMPS = mount_graph()
    mount_page(HTML, COMPS)
