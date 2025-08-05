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
    
    def get_type(self, obj):
        if 'float' in obj.lit:
            return obj.lit
        if 'numebr' in obj.lit:
            return obj.lit
        if 'char' in obj.lit:
            return obj.lit
        if obj.lit == 'call':
            bin = self.char.at(obj.child[0].lit)
            for i in obj.child[0].child:
                self.get_type(i)
                
            print(obj.child[0].lit)
            return bin["type"]
                 
                
    
    def __call__(self) -> list[node]:
        self.vars()
        self.funcs()
        return self.char