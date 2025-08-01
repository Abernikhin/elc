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
                if stokens[i].lit == ';':
                    break
                tokens.append(stokens[i])
            for i in range(len(tokens)+2):
                self.tokens.pop(0)
            return self.let(tokens)
        
        if stokens[0] == "function":
            for i in range(1, len(stokens)):
                if stokens[i].lit == ';':
                    break
                if stokens[i].lit == '{':
                    is_impl = True
                    break
                tokens.append(stokens[i])
            for i in range(len(tokens)+2):
                self.tokens.pop(0)
                    
            return self.func(tokens)
        
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
        
        # elif stokens[1] == '(':
        #     for i in range(len(stokens)):
        #         if stokens[i].lit == ';':
        #             break
        #         tokens.append(stokens[i])
        #     for i in range(len(tokens)+1):
        #         self.tokens.pop(0)

        #     n = node(token("name", "call"), node(tokens[0]))
        #     tokens.pop(0)
        #     expr = []
        #     buf = []
        #     tokens.pop(0)
        #     tokens.pop()
        #     for i in tokens:
        #         if i == ',':
        #             expr.append(buf)
        #             buf = []
        #             continue
        #         buf.append(i)
        #     expr.append(buf)
        #     for i in expr:
        #         n.append(self.expr(i))
        #     return n
                   

                
    
    def import_module(self, tokens):
        e = ''
        for i in tokens:
            e += i.lit
        return node(token("name", "import"), node(token("name", e))) # type: ignore

    def let(self, tokens):
        result = node(token("name", "let"))
    
        n = node(token("name", "none"))
        if tokens[1] == ':':
            n = node(tokens[1], node(tokens[0]))
            tp = []
            for t in range(2, len(tokens)):
                if tokens[t] == '=':
                    break
                tp.append(tokens[t])
            for t in range(len(tp)+2):
                tokens.pop(0) # type: ignore
            n.append(self.type(tp))
        else:
            n = node(token("op:", ':'), node(tokens[0]), node(token("name", "auto")))

        if len(tokens) == 0: # type: ignore
            return n
        if tokens[0].type == "name":
            tokens.pop(0)
        n = node(tokens[0], n)
        tokens.pop(0)
        n.append(self.expr(tokens))
        return node(token("name", "let"), n)
    
    def func(self, tokens: list):
        n = node(tokens[0])
        tokens.pop(0)
        if len(tokens) == 0:
            if len(tokens) == 0:
                n.append(node(token("op:", ":"), node(token("name", "void"))))
                return node(token("name", "function"), n)
        if tokens[0] == "(":
            tokens.pop(0)
            buf = []
            args = node(token("op()", "()"))
            for i in tokens.copy():
                tokens.pop(0)
                if i == ')':
                    if buf != []:
                        if len(buf) > 2:
                            args.append(self.let(buf))
                            buf = []
                        else:
                            args.append(node(buf[0]))
                    break
                if i == ',':
                    if len(buf) > 2:
                        args.append(self.let(buf))
                        buf = []
                    else:
                        args.append(node(buf[0]))
                    continue
                buf.append(i)
            n.append(args)
            if len(tokens) == 0:
                n.append(node(token("op:", ":"), node(token("name", "void"))))
                return node(token("name", "function"), n)
            if tokens[0] == ':':
                n.append(node(token("op:", ":"), node(tokens[1])))
                return node(token("name", "function"), n)
        if tokens[0] == ':':
            n.append(node(token("op:", ":"), node(tokens[1])))
            return node(token("name", "function"), n)
                
                    
        

    def type(self, tokens):
        return node(tokens[0])
    

    def expr(self, tokens, mode = True):
        if 0 < len(tokens) < 3:
            return self.unary(tokens)
        index = 0
        if mode:
            tokens.reverse()
        c = 0
        for i in tokens: # type: ignore
            if i in ['(', ')']:
                if c%2 == 0:
                    c += 1
                else:
                    c -= 1
                continue
            if c != 0:
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
        if 0 < len(tokens) < 3:
            return self.unary(tokens)
        index = 0
        if mode:
            tokens.reverse()
        c = 0
        skip = True
        for i in tokens: # type: ignore
            if tokens[0] == '*' and skip:
                skip = False
                continue
            if i in ['(', ')', '[', ']']:
                if c%2 == 0:
                    c += 1
                else:
                    c -= 1
                index += 1
                continue
            if c != 0:
                index += 1
                continue
            if i in ['*', '/', '%']:
                n = node(i) # type: ignore

                tok = []
                for t in range(index+1, len(tokens)):
                    tok.append(tokens[t])
                n.append(self.term(tok, False)) # type: ignore
                tok = []
                for t in range(0, index):
                    tok.append(tokens[t])
                n.append(self.term(tok, False)) # type: ignore
                return n
            index += 1
        else:
            return self.unary(tokens)
    
    def unary(self, tokens: list[token]):
        if len(tokens) == 0:
            return node(token("error", "error"))
        if tokens[0] in ['(', ')']:
            tokens.pop(0)
            return self.expr(tokens)
        if len(tokens) > 2:
            if tokens[0].type == "name":
                if tokens[1] in ['.', '->']:
                    if len(tokens) == 3:
                        return node(tokens[1], node(tokens[0]), node(tokens[2]))
                if tokens[1] in ['(', ')']:
                    expr = []
                    buf = []
                    for i in range(2, len(tokens)-1):
                        if tokens[i] == ',':
                            expr.append(buf)
                            buf = []
                            continue
                        buf.append(tokens[i])
                    if buf != []:
                        expr.append(buf)
                    n = node(tokens[0])
                    for i in expr:
                        n.append(self.expr(i))
                    return node(token("op()", '()'), n)
                if tokens[1] in ['[', ']']:
                    expr = []
                    for i in range(2, len(tokens)-1):
                        expr.append(tokens[i])
                    n = node(tokens[0])
                    n.append(self.expr(expr))
                    return node(token("op[]", '[]'), n)
        return node(tokens[0])