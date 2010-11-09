# ... simulate java like output in str()
_str = str
def str(o):
    if o is None:
        return ""
    elif o is True:
        return "true"
    elif o is False:
        return "false"
    elif isinstance(o,unicode):
        return o.encode('utf8')
    else:
        return _str(o)
        
# >>> operator
def bsr(value, bits):
    """ bsr(value, bits) -> value shifted right by bits

    This function is here because an expression in the original java
    source contained the token '>>>' and/or '>>>=' (bit shift right
    and/or bit shift right assign).  In place of these, the python
    source code below contains calls to this function.

    Copyright 2003 Jeffrey Clement.  See pyrijnadel.py for license and
    original source.
    """
    minint = -2147483648
    if bits == 0:
        return value
    elif bits == 31:
        if value & minint:
            return 1
        else:
            return 0
    elif bits < 0 or bits > 31:
        raise ValueError('bad shift count')
    tmp = (value & 0x7FFFFFFE) // 2**bits
    if (value & minint):
        return (tmp | (0x40000000 // 2**(bits-1)))
    else:
        return tmp        
            
def bsl(value,bits):
    raise NotImplemented
        
class synchronize(object):
    def __init__(self,lock):
        pass
    
    def __enter__(self,*a):
        #print "__enter__",a
        pass
        
    def __exit__(self,*a):
        #print "__exit__",a
        pass

def java_module(module):
    """Replaces submodules of the given module with their main classes, 
    so that e.g. com.someorg.someclass.someclass (the class) is accessible at 
    com.someorg.someclass (where python would put the module). 
    
    This is a blatant monkeypatch but it works."""
    
    for name in dir(module):
        if name[0:2] != '__':
            sub = module.__getattribute__(name)
            if isinstance(sub,type(module)):
                try:
                    module.__setattr__(name,sub.__getattribute__(name))
                except AttributeError:
                    pass
                    
class ThisPackage(object):
    """If SomeClass is in globals(), then thispackage.x.y.z.SomeClass == SomeClass
    
    This is an even dirtier monkeypatch than the previous"""
    def __getattr__(self,name):
        g = globals()
        if name in g:
            return g[name]
        else:
            return self
        
def set_this_package(pathstr):
    """Put a ThisPackage instance at the first point in pathstr which is still undefined"""
    path = pathstr.split('.')
    pterm, path = path[0], path[1:]
    if pterm not in globals():
        #TODO: check if this works in pyjamas - figure a fix if it doesn't. 
        #(It's valid python but might not translate well into javascript)
        globals()[pterm] = ThisPackage()
        return
    here = globals()[pterm]
    for pterm in path:
        new_here = getattr(here, pterm, None)
        if new_here is None:
            here.__setattr__(pterm, ThisPackage())
            return
        here = new_here
        
    #If we get here, there are imports from the same package.
    #So, we must monkeypatch the package to act like ThisPackage.
    #This is the dirtiest monkeypatch of all.
    here.__getattr__ = ThisPackage.__getattr__