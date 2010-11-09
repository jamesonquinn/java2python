#!/usr/bin/env python
#-*- coding:utf-8 -*-

import aterm
import sys
import yaml
import os
from j2pyconfig import config
import simplify

"""
rename packages
"""

DEBUG = False

conversions = config["rename-packages"]

def rename_pkg(pkg,module=None):
    """
    applies configured translations to pkg
    returns translated pkg name
    """

    if module is not None:
        module = "%s.%s" % (pkg,module)

    for m,r in conversions.iteritems():
        if pkg == m or module == m: return r
        if pkg.startswith(m): return r + pkg[len(m):]

    return module


def translate_packages(ast):
    for p in ast.findall("TypeImportDec"):
        if DEBUG:
            print p
        if len(p)==1 and p[0][0].name=="Id":
            pkg = p[0][0][0]
            module = p[0][1][0]
            rpkg = rename_pkg(pkg,module)
            if rpkg != pkg:
                p[0][0].replace(aterm.decode('Id("%s")' % (rpkg)) )
                if DEBUG:
                    print pkg,"-->",p[0][0]
                    print " ",p
        
        #import a second time so fully-qualified name works too
        reimport = aterm.decode('Id("import %s")' % pkg)
        p.add_after(reimport)
        reimport.add_after(aterm.decode('Id("java_module(%s)")' % pkg))
        
    for p in ast.findall("PackageDec"):
        packagePath = '.'.join([id[0] for id in p[1][0]])
        packagePath = rename_pkg(packagePath)
        baseName = packagePath.split(".")[0]
        
        parents = [p for p in p.parents()]
        if parents[0].name == "Some":
            putafter = parents[0]
        else:
            putafter = p
        for q in ast.findall(("TypeImportOnDemandDec", "TypeImportDec")):
            putafter = q.up
            
        up = putafter.up
        after = up[putafter.pos()+1]
        after.append(aterm.decode(r'Id("java.set_this_package(\"%s\")")' % packagePath)) 
        #actually, add_before with inc of 2 is really add 2 after.
        

run = translate_packages


if __name__ == '__main__':

    if DEBUG:
        print "conversions", conversions

    ast = aterm.decode(sys.stdin.read())
    simplify_names(ast)
    translate_packages(ast)
    if not DEBUG:
        print ast
