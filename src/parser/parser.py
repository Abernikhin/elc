from parser.node import node, token

class parser:
    def __init__(self, tokens: list[token]) -> None:
        self.tokens = tokens
        self.result = []
    
    def __call__(self):
        while len(self.tokens) > 0:
            self.result.append(self.rout(self.tokens))
        return self.result
    
    def rout(self, stokens, func_loc = False):
        tokens = []
        if stokens[0] == "let":
            tokens = []
            for i in range(1, len(self.tokens)):
                if self.tokens[i] == ';':
                    break
                tokens.append(self.tokens[i])
            for i in range(len(tokens)+2):
                self.tokens.pop(0)
            return self.let(tokens)
    
    def let(self, tokens):
        n: node
        if tokens[1] == ':':
            n = node(tokens[1], node(tokens[0]), )
            buf = []
            for i in range(2, len(tokens)):
                if tokens[i] == '=':
                    break
                buf.append(tokens[i])
            for i in range(len(buf)+2):
                tokens.pop(0)
            n.append(self.factor(buf))
            if len(tokens) == 0:
                n = node(token('op=', '='), n, node(token("name", 'null')))
                return n
            tokens.pop(0)
            if len(tokens) == 0:
                n = node(token('op=', '='), n, self)
                return n

            elif tokens[0] == '=':
                tokens.pop(0)
                n.append(self.factor(tokens))
                return n
        
        if tokens[1] == '=':
            n = node(tokens[1], node(token('op:', ':'), node(tokens[0]), node(token('name', 'auto'))))
            buf = []
            tokens.pop(0)
            tokens.pop(0)
            n.append(self.factor(tokens))
            return n

    def factor(self, tokens):
        if tokens[0] == '(':
            if tokens[-1].type == "name":
                buf = []
                for i in range(1, len(tokens)-1):
                    buf.append(tokens[i])
                return node(token("name", "convert"), node(tokens[-1]), self.factor(buf))
        return node(tokens[0])