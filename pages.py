# -*- coding: utf-8 -*
import jinja2


def out_index(pages):
    templateLoader = jinja2.FileSystemLoader(searchpath="./templates")

    templateEnv = jinja2.Environment(loader=templateLoader)

    template = templateEnv.get_template("./template.html")

    templateVars = {"pages": pages}

    with open('index.html', 'w') as rp:
        rp.writelines(template.render(templateVars))
