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
        
        elif stokens[0] == "function":
            pass
        
        elif stokens[0] == "import":
            for i in range(1, len(stokens)):
                if stokens[i].lit == ';':
                    break
                tokens.append(stokens[i])
            for i in range(len(tokens)+2):
                self.tokens.pop(0)
            return self.import_module(tokens)
    
    def import_module(self, tokens):
        e = ''
        for i in tokens:
            e += i.lit
        return node(token("name", "import"), node(tokens[0]))

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
            
            n = node(i[0], n)
            i.pop(0)
            n.append(self.expr(i))
            result.append(n)
            continue
        
        return result
    
    def func(self, tokens):
        pass

    def type(self, tokens):
        if len(tokens) == 1:
            return node(tokens[0])

    def oc(self, tokens):
        if len(tokens) == 1:
            return tokens
        result = []
        buf  = []
        index = 0
        c = 0
        while index < len(tokens):
            i = tokens[index]
            if i == '(' or i == '[':
                if c != 0:
                    buf.append(i)
                c += 1
            elif i == ')' or i == ']':
                c -= 1
                if c == 0:
                    result.append(buf)
                    buf = []
                else:
                    buf.append(i)
                index += 1
                continue
            elif c != 0:
                buf.append(i)
            elif c == 0:
                result.append(i)
            index += 1
            
        return result
    
    def expr(self, tokens, mode = True):
        if len(tokens) < 3:
            return self.unary(tokens)
        index = 0
        tokens = self.oc(tokens) # type: ignore
        if mode:
            tokens.reverse()
        for i in tokens: # type: ignore
            if type(i) == list:
                index += 1
                continue
            if i in ['+', '-']:
                n = node(i) # type: ignore

                tok = []
                for t in range(index+1, len(tokens)):
                    tok.append(tokens[t])
                n.append(self.expr(tok, False)) # type: ignore
                tok = []
                for t in range(0, index):
                    tok.append(tokens[t])
                n.append(self.expr(tok, False)) # type: ignore
                return n
            index += 1
        else:
            return self.term(tokens)

    
    def term(self, tokens, mode = True):
        if len(tokens) < 3:
            return self.unary(tokens)
        index = 0
        tokens = self.oc(tokens) # type: ignore
        if mode:
            tokens.reverse()
        for i in tokens: # type: ignore
            if type(i) == list:
                index += 1
                continue
            if i in ['*', '/']:
                n = node(i) # type: ignore

                tok = []
                for t in range(index+1, len(tokens)):
                    tok.append(tokens[t])
                n.append(self.expr(tok)) # type: ignore
                tok = []
                for t in range(0, index):
                    tok.append(tokens[t])
                n.append(self.expr(tok)) # type: ignore
                return n
            index += 1
        else:
            return self.unary(tokens)

    def unary(self, tokens):
        # breakpoint()
        if len(tokens) == 1:
            if type(tokens[0]) == list:
                if len(tokens[0]) == 1:
                    return node(tokens[0][0])
                return self.expr(tokens[0])
        return node(tokens[0])
        # return node(token("error", "error"))