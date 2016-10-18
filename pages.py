# -*- coding: utf-8 -*
from jinja2 import FileSystemLoader, Environment


def out_index(pages):
    temp_path = FileSystemLoader(searchpath="./templates")

    j_env = Environment(loader=templateLoader)

    template = templateEnv.get_template("./template.html")

    templateVars = {"pages": pages}

    with open('index.html', 'w') as rp:
        rp.writelines(template.render(templateVars))
