from parser.node import*

class char:
    def __init__(self) -> None:
        self.vars = []
        self.funcs = []
    
    def add_var(self, branch: node):
        if branch.lit == '=':
            self.vars.append({"name": branch.child[0].child[0].lit, "type": branch.child[0].child[1].lit})
            if branch.child[0].child[1].lit == 'auto':
                if branch.child[1].type == 'number':
                    self.vars[-1]["type"] = 'number'
                if branch.child[1].type == 'char':
                    self.vars[-1]["type"] = 'char'
                if branch.child[1].type == 'float':
                    self.vars[-1]["type"] = 'float'
                        
    
    def add_func(self, branch: node):
        name = branch.lit
        ret = "void"
        args = []
        for i in branch.child:
            if i.lit == "args":
                for c in i.child:
                    args.append(c.child[1])
            if i.lit == ":":
                ret = i.child[0].lit
        
        self.funcs.append({"name": name, "return": ret, "args": args})
