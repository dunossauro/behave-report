from re import compile, MULTILINE, DOTALL
from collections import Counter
from bokeh.plotting import figure
from bokeh.embed import file_html
from bokeh.resources import CDN
from numpy import pi
from sys import argv

colors = {
    'failed': 'red',
    'passed': 'green',
    'skipped': 'blue',
}

# Baseic regex
remove_scenarios = compile(
    "@scenario.begin(.*?)@scenario.end", MULTILINE | DOTALL)
scenarios = compile("Cenário: .*|Contexto: .*")
steps = compile("\s+(.*?) ... (failed|passed|skipped) in (.*)")

# lista de tuplas que vão formar o gráfico final
_results = []

# lista dos htmls
filo = []


def mount_page(html):
    """
    Função que pega os dados colocados na fila e grava no arquivo
    """
    html.write('</div>\n')
    for x in filo:
        html.write(x)

def grap(html):
    """
    Função que gera o gráfico de pizza a partir de un dicionário
    """
    t = sum(x[1] for x in _results)

    passed = sum([x[0]['passed'] for x in _results])
    failed = sum([x[0]['failed'] for x in _results])
    skipped = sum([x[0]['skipped'] for x in _results])

    percents = [skipped / t,
                passed / t,
                failed / t]

    colors_ = ['green', 'blue', 'red']
    starts = [p * 2 * pi for p in percents[:-1]]
    ends = [p * 2 * pi for p in percents[1:]]

    p = figure(x_range=(-1, 1), y_range=(-1, 1))

    p.wedge(x=0, y=0, radius=1, start_angle=starts,
            end_angle=ends, color=colors_)

    html.write(file_html(p, CDN))


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


def get_scenarios(xml):
    """
    Função que itera no xml e busca os cenários
    E chama a função para retornar os steps ao cenário relacionado
    """
    for test in remove_scenarios.findall(xml):
        cen = scenarios.findall(test)
        filo.append('<h4>' + "".join(cen) + '</h4>\n')

        get_steps(test)


def get_steps(test):
    """
    Função que é chamada por get_scenarios e itera na saida do xml
    Em sequência chama a função de métricas
    """
    out = steps.findall(test)
    for x in out:
        topics = x[0].split()
        text = " ".join(topics[1:])

        filo.append(
            '<b>{}</b> {}<font color="{}"> {}</font> in {}\n'.format(
                topics[0],
                text,
                colors[x[1]],
                x[1],
                x[2]))
        filo.append('<br>')
    metrics(out)


def metrics(out):
    """
    Função responsável por extrair o estado do step (failed, passed, skipped)
    """
    results = len(out)
    dic = Counter([x[1] for x in out])
    if dic['failed'] != 0:
        color = colors['failed']
        status = 'FAILED'

    elif dic['skipped'] > 0:
        color = colors['skipped']
        status = 'SKIPPED'

    else:
        color = 'green'
        status = 'PASSED'

    if dic['passed'] == results:
        filo.append('<br>\
        <b>\
        <font color="{}">{}</font>\
        </b>\n'.format(color, status))

    else:
        filo.append('<br>\
        <b>\
        <font color="{}">{} {} steps:</font>\
        </b>\n'.format(color, status, results))
        for x in dic:
            filo.append("<br> {}: {}\n".format(dic[x], x))

    _results.append((dic, sum(dic.values())))

if __name__ == '__main__':
    # --- leitura da entrada
    xml = open(argv[1]).read()
    html = open(argv[2], 'w')

    # -- code
    get_scenarios(xml)
    head(html)
    grap(html)
    mount_page(html)

    # --- fecha o arquivo
    html.close()
