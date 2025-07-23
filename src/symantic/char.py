from parser.node import*

class char:
    def __init__(self) -> None:
        self.vars = []
        self.funcs = []
    
    def add_var(self, branch: node):
        if branch.lit == ":":
            self.vars.append([branch.child[0].lit, branch.child[1].lit])
        elif branch.lit == '=':
            self.vars.append({"name": branch.child[0].child[0].lit, "type": branch.child[0].child[1].lit})
    
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
