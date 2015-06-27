import lang.gbs_constructs

class JSGbsCode(object):
    
    def __init__(self, tree, prfn, name=None, params=["t"], explicit_board=True):
        self.tree = tree
        self.prfn = prfn
        self.name = name
        self.params = params
        self.ops = []
        self.label_table = {}
        self.nearby_elems = {}
        self.explicit_board = explicit_board
        
    def is_function(self):
        return self.prfn == 'function'
    
    def is_procedure(self):
        return self.prfn == 'procedure'
    
    def is_entrypoint(self):
        return self.prfn == 'entrypoint'
    
    def push(self, op, near=None):
        if near:
            self.nearby_elems[len(self.ops)] = near
        self.ops.append(op)
    
    def build_label_table(self):
        pass
      
    def add_enter(self):
        pass
        #if self.prfn == 'function':
        #    self.push(('enter',))
      
    def add_leave_return(self):
        if self.prfn == 'entrypoint' and self.name == 'program':
            self.add_leave_return_to_entrypoint()
        elif len(self.ops) == 0 or self.ops[-1][0] != 'return':
            assert self.prfn == 'procedure'
            if self.explicit_board:
                pass #self.push(('return', 1))
            else:
                pass #self.push(('return', 0))
        elif len(self.ops) > 0 and self.ops[-1][0] == 'return' and self.prfn == 'function':
            pass
            #self.ops.insert(-1, ('leave',))
      
    def add_leave_return_to_entrypoint(self):
        if len(self.ops) == 0 or self.ops[-1][0] != 'returnVars':
            self.push(('returnVars',))
      
    def construct(self):
        if self.prfn == 'function':
            return lang.gbs_constructs.UserCompiledFunction(self.name, self.params)
        else:
            return lang.gbs_constructs.UserCompiledProcedure(self.name, self.params)
  
    def __repr__(self):
        def showop(op):
            if isinstance(op, tuple):
                return op[0] + "(" + ', '.join([str(x) for x in op[1:]]) + ");"
            else:
                return op

        params = ", ".join(self.params)
        if self.prfn == 'function':
            _def = "var " + self.name + " = declareFunction(function (%s) {\n%s\n})"
        elif self.prfn == 'lambda':
            _def = "function (%s) {\n%s\n}" 
        else:
            _def = "function " + self.name +"(%s) {\n%s\n}"
            
        full = _def % (params, "\t" + "\n\t".join([showop(x) for x in self.ops]),)
        return full        
    
    
    