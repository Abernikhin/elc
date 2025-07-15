from lexer.token import*

class node:
    def __init__(self, lit: token, *child, tag: str|None = None) -> None:
        self.lit = lit.lit
        self.type = lit.type
        self.child: list[node] = list(child)
    
    def append(self, obj):
        self.child.append(obj)

    def __eq__(self, value: str) -> bool: # type: ignore
        if self.type == value:
            return True
        return False