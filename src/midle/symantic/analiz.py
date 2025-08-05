from midle.symantic.char import*

class analizer:
    def __init__(self, ast):
        self.char = char()
        self.ast = ast
    
    def vars(self) -> None:
        for i in self.ast:
            if i == 'let':
                self.char.add_var(i.child[0])
    
    def funcs(self) -> None:
        for i in self.ast:
            if i == 'fun':
                self.char.add_func(i.child[0])
    
    def types(self) -> None:
        for i in self.ast:
            if i == 'let':
                self.char[i.child[0].child[0].child[0].lit] = self.get_type(i.child[0].child[1])
    
    def get_type(self, obj):
        if obj.type == 'float':
            return "float"
        if obj.type == 'number':
            return "number"
        if obj.type == 'char':
            return "char"
        if obj.lit == 'call':
            bin = self.char.at(obj.child[0].lit)
            for i in obj.child[0].child:
                self.get_type(i)
                
            print(obj.child[0].lit)
            return bin["type"]
                 
                
    
    def __call__(self) -> list[node]:
        self.vars()
        self.types()
        self.funcs()
        return self.char