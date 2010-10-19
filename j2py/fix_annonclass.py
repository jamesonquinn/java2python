import aterm

"""
handle annonymous classes
"""
anon_class_name = "__AnonClass__"
class_dec = '''
ClassDec(
  ClassDecHead(
    [Public(), Final()]
    , Id("'''+anon_class_name+'''")
    , None()
    , None()
    , None()
  )
  , ClassBody())
'''
    

    
can_add_classdec = ("Block",)

@aterm.transformation
def fix_annonclass(ast):
    for ni in ast.findall('NewInstance'):
        ##print "QQQQ", ni[3]
        if ni[3].name == "Some":
          
            for p in ni.parents():
                if p.name in can_add_classdec:
                    #add declaration for anon class
                    cblock = aterm.decode(class_dec)
                    cblock[1].extend(ni[3][0].copy())
                    p[0].insert(0,cblock)
                    
                    #remove inline declaration
                    while True:
                      try:
                        ni.pop()
                      except:
                        break
                    ni.name = "Id"
                    ni.append(anon_class_name)
        
    return ast

    
def run(ast):
    return fix_annonclass(ast)

    
    
