from parser.node import node, token

class parser:
    def __init__(self, tokens: list[token]) -> None:
        self.tokens = tokens
        self.result = []
    
    def __call__(self):
        while len(self.tokens) > 0:
            self.result.append(self.rout(self.tokens))
        return self.result
    
    def rout(self, stokens):
        tokens = []
        if stokens[0] == "let":
            for i in range(1, len(stokens)):
                tokens.append(stokens[i])
                if stokens[i].lit == ';':
                    break
            for i in range(len(tokens)+1):
                self.tokens.pop(0)
            return self.let(tokens)
        
        elif self.tokens[0] == "function":
            pass

    def let(self, tokens):
        result = node(token("name", "let"))
        expr = []
        buf = []
        for i in tokens:
            if i == ";" or i == ',':
                expr.append(buf)
                buf = []
                continue
            buf.append(i)
        
        for i in expr:
            n = node(token("name", "none"))
            if i[1] == ':':
                n = node(i[1], node(i[0]))
                tp = []
                for t in range(2, len(i)):
                    if i[t] == '=':
                        break
                    tp.append(i[t])
                for t in range(len(tp)+2):
                    i.pop(0) # type: ignore
                n.append(self.type(tp))
            else:
                n = node(token("op:", ':'), node(i[0]), node(token("name", "auto")))
    
            if len(i) == 0: # type: ignore
                result.append(n)
                continue
        
        return result
    
    def func(self, tokens):
        pass

    def type(self, tokens):
        if len(tokens) == 1:
            return node(tokens[0])
