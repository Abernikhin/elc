from parser.node import*
from symantic.char import*

class gc:
    def ganare(self, ast: list[node], t: char) -> str:
        target = ""
        for i in ast:
            if i == 'let':
                obj = t[i.child[0].child[0].child[0].lit]
                if obj["type"] in ["number", "char", "float"]:
                    target += f"{obj["name"]} = push({self.expr(i.child[0].child[1])})\n"
        
        return target
    
    def expr(self, obj):
        if obj == "call":
            result = f"{obj.child[0].lit}("
            for i in obj.child[0].child:
                result += self.expr(i)
            result += ')'
            return result
        return obj.lit