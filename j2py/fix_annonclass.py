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
    , Id("object")
    , None()
  )
  , ClassBody())
'''
    
class_make_instance = '''NewInstance(
                          None()
                        , ClassOrInterfaceType(TypeName(Id("'''+anon_class_name+'''")), None())
                        , []
                        , None()
                        )'''

##Invoke(Class(TypeName(Id(""))), [])
    
can_add_classdec = ("Block",)

def MemoryIter(seed, iter):
    b = seed
    for i in iter:
        a, b = b, i
        yield a, b

@aterm.transformation
def fix_annonclass(ast):
    for ni in ast.findall('NewInstance'):
        ##print "QQQQ", ni[3]
        if ni[3].name == "Some":
          
            for pc, p in ni.parents():
                if p.name in can_add_classdec:
                    #add declaration for anon class
                    cblock = aterm.decode(class_dec)
                    cblock[1].extend(ni[3][0].copy())
                    pc.add_before(cblock)
                    
                    #remove inline declaration
                      
                    nblock = aterm.decode(class_make_instance)
                    ni.replace(nblock)
        
    return ast

    
def run(ast):
    return fix_annonclass(ast)

    
    
