from lexer.token import*

class node:
    def __init__(self, lit: token, *child, tag: str|None = None) -> None:
        self.lit = lit.lit
        self.type = lit.type
        self.child: list[node] = list(child)
    
    def append(self, obj):
        self.child.append(obj)

    def __eq__(self, value: str) -> bool: # type: ignore
        if self.lit == value:
            return True
        return False
    
    def info(self, c = 0):
        print('   '*c+'|~ '+self.lit)
        for i in self.child:
            i.info(c+1)