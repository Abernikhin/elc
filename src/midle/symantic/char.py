from front.parser.node import*

class char:
    def __init__(self) -> None:
        self.vars = [
            
        ]
        self.funcs = [
            
        ]
    
    def __getitem__(self, name):
        for i in self.vars:
            if i["name"] == name:
                return i
    
    def __setitem__(self, name, type):
        index = 0
        for i in self.vars:
            if i["name"] == name:
                self.vars[index]["type"] = type
            index += 1
    
    def at(self, name):
        for i in self.funcs:
            if i["name"] == name:
                return i
    
    def add_var(self, branch: node):
        if branch.lit == '=':
            self.vars.append({"name": branch.child[0].child[0].lit, "type": branch.child[0].child[1].lit})
            print("run", self.vars[-1])
    
    def add_func(self, branch: node):
        name = branch.lit
        ret = "void"
        args = []
        for i in branch.child:
            if i.lit == "args":
                for c in i.child:
                    if c == ':':
                        args.append(c.child[1].lit)
                        continue
                    args.append(c.lit)
            if i.lit == ":":
                ret = i.child[0].lit
        
        self.funcs.append({"name": name, "type": ret, "args": args})
