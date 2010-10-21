#-*- coding:utf-8 -*-

import config
import aterm
import logging

logger = logging.getLogger("j2py.fix_expressions")

assign_expressions = config.config["assign-expressions"]

pre_expressions = ["PreIncr","PreDecr"]
post_expressions = ["PostIncr","PostDecr"]

@aterm.transformation
def fix_assigns(ast):
    for a in ast.findall(assign_expressions):
        parents = [ p for p in a.parents() ]
        if parents[0].name != 'ExprStm':
            logging.warning("inner assign %s %s",a, [p.name for p in parents])
            if a.name in pre_expressions + post_expressions:
                stems = [p for p in parents if p.name=='ExprStm']
                if stems:
                    logging.warning("fixing inner assign %s %s",a, [p.name for p in parents])
                    if a.name in pre_expressions:
                        stems[0].add_before(a.copy())
                    else:
                        stems[0].add_after(a.copy())
                    a.replace(a[0])

run = fix_assigns
