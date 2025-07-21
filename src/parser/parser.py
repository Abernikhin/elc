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
            for i in range(1, len(stokens)):
                tokens.append(stokens[i])
                if stokens[i].lit == ';':
                    break
            for i in range(len(tokens)+1):
                self.tokens.pop(0)
            return self.let(tokens)
        
        elif not func_loc:
            if stokens[0] == "function":
                is_impl = False
                impl = []
                for i in range(1, len(stokens)):
                    if stokens[i].lit == ';':
                        break
                    if stokens[i].lit == '{':
                        is_impl = True
                        break
                    tokens.append(stokens[i])
                        
                for i in range(len(tokens)+2):
                    self.tokens.pop(0)
                n = self.func(tokens)
                if is_impl:
                    i = node(token("name", "impl"))
                    while self.tokens[0] != '}':
                        i.append(self.rout(self.tokens, True))
                    self.tokens.pop(0)
                    n.append(i)
                        
                return n
        
        elif stokens[0] == "import":
            for i in range(1, len(stokens)):
                if stokens[i].lit == ';':
                    break
                tokens.append(stokens[i])
            for i in range(len(tokens)+2):
                self.tokens.pop(0)
            return self.import_module(tokens)
        
        elif stokens[0] == "return":
            for i in range(0, len(stokens)):
                if stokens[i].lit == ';':
                    break
                tokens.append(stokens[i])
            for i in range(len(tokens)+1):
                self.tokens.pop(0)
            n = node(tokens[0])
            tokens.pop(0)
            n.append(self.expr(tokens))
            return n
        
        elif stokens[1] == '(':
            for i in range(len(stokens)):
                if stokens[i].lit == ';':
                    break
                tokens.append(stokens[i])
            for i in range(len(tokens)+1):
                self.tokens.pop(0)

            n = node(tokens[0])
            tokens.pop(0)
            expr = []
            buf = []
            tokens.pop(0)
            tokens.pop()
            for i in tokens:
                if i == ',':
                    expr.append(buf)
                    buf = []
                    continue
                buf.append(i)
            expr.append(buf)
            for i in expr:
                n.append(self.expr(i))
            return n
                   

                
    
    def import_module(self, tokens):
        e = ''
        for i in tokens:
            e += i.lit
        return node(token("name", "import"), node(token("name", e))) # type: ignore

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
        tokens = self.oc(tokens)
        n = node(tokens[0])
        tokens[1].append(token("semicolon", ';'))
        if len(tokens[1]) > 1:
            args = node(token("name", "args"), self.let(tokens[1]))
            n.append(args)
            if len(tokens) > 3:
                r = node(tokens[2])
                tp = []
                for i in range(3, len(tokens)):
                    tp.append(tokens[i])
                r.append(self.type(tp))
                n.append(r)
            else:
                n.append(node(token("op:", ":"), node(token("name", "void"))))
        return n

    def type(self, tokens):
        tokens = self.oc(tokens)
        if type(tokens[0]) == list:
            return self.union(tokens[0])
        return node(tokens[0])

    def union(self, tokens: list[token]):
        buf = []
        expr = []
        #breakpoint()
        tokens = self.oc(tokens)
        for i in tokens:
            if i == '|':
                expr.append(buf)
                buf = []
                continue
            buf.append(i)
        expr.append(buf)
        n = node(token("name", "union"))
        for i in expr:
            n.append(self.type(i))
        
        return n

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
    
    def fi(self, tokens):
        if len(tokens) == 1:
            return tokens
        result = []
        buf  = []
        index = 0
        c = 0
        while index < len(tokens):
            i = tokens[index]
            if i == '{':
                if c != 0:
                    buf.append(i)
                c += 1
            elif i == '}':
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