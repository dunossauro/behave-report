# -*- coding: utf-8 -*
from jinja2 import FileSystemLoader, Environment
from os import listdir


def out_index(pages):
    temp_path = FileSystemLoader(searchpath="./templates")

    j_env = Environment(loader=temp_path)

    template = j_env.get_template("./index.html")

    templateVars = {"pages": pages}

    with open('index.html', 'w') as rp:
        rp.writelines(template.render(templateVars))

# Implentação futura
# provavelmente seja usada com click

pages = [x[:-5] for x in listdir('.') if x[-4:] == 'html' and
         x != "index.html"]

out_index(pages)
