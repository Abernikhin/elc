from midle.symantic.char import*

class analizer:
    def __init__(self, ast):
        self.char = char()
        self.ast = ast
    
    def vars(self) -> None:
        for i in self.ast:
            if i == 'let':
                self.char.add_var(i.child[0])
    
    def __call__(self) -> list[node]:
        self.vars()
        return self.char