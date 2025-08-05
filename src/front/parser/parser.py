from front.parser.node import node, token

class token_list:
    def __init__(self, sig):
        self.sig = sig
        self.e = []
    
    def append(self, obj):
        self.e.append(obj)
    
    def __getitem__(self, index):
        return self.e[index]

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
            return node(token("name", "let"), self.let(tokens))
        if stokens[0] == "fun":
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
            n = self.fun(tokens)
            if is_impl:
                i = node(token("name", "impl"))
                while self.tokens[0] != '}':
                    i.append(self.rout(self.tokens, True))
                self.tokens.pop()
                n.append(i)
                    
            return node(token("name", "fun"), n)
                
        raise KeyboardInterrupt
            

    def type(self, tokens):
        _type = ""
        for i in tokens:
            _type += i.lit
        return node(token("name", _type))

    def fun(self, tokens):
        tokens = self.parent(tokens)
        n = node(tokens[0])
        args = node(token("name", "args"))
        del tokens[0]
        index = 0
        for i in tokens:
            if type(i) == token_list:
                buf = []
                expr = []
                for a in i.e:
                    if a == ',':
                        expr.append(buf)
                        buf = []
                        continue
                    buf.append(a)
                if buf != []:
                    expr.append(buf)
                for a in expr:
                    no_name = True
                    for b in a:
                        if b == ':':
                            no_name = False
                            break
                    if no_name:
                        args.append(self.type(a))
                    else:
                        args.append(node(a[1], node(a[0]), self.type(a[2:])))
            elif i == ':':
                n.append(node(i, node(tokens[index+1])))
                break
            index += 1
        n.append(args)
        return n

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
            n.append(self.type(buf))
            if len(tokens) == 0:
                n = node(token('op=', '='), n, node(token("name", 'null')))
                return n
            tokens.pop(0)
            n = node(token('op=', '='), n, self.expr(tokens))
            return n
        
        if tokens[1] == '=':
            n = node(tokens[1], node(token('op:', ':'), node(tokens[0]), node(token('name', 'auto'))))
            buf = []
            tokens.pop(0)
            tokens.pop(0)
            n.append(self.expr(tokens))
            return n


    def parent(self, tokens):
        result = []
        buf    = token_list(0)
        bufs   = token_list(1)
        typep  = 0
        index  = 0
        c      = 0
        while index < len(tokens):
            i = tokens[index]
            if i == '(':
                if c != 0:
                    buf.append(i)
                c += 1
                index += 1
                continue
            if i == ')':
                c -= 1
                index += 1
                if c != 0:
                    buf.append(i)
                if c == 0:
                    result.append(buf)
                    buf = token_list(0)
                continue
            if c != 0:
                buf.append(i)
                index += 1
                continue
            result.append(i)
            index += 1
        return result

                
    def expr(self, tokens, rev = True, level = 0):
        index = -1
        tokens = self.parent(tokens)
        if rev:
            tokens.reverse()
        for i in tokens: # operators + and -
            index += 1
            if type(i) == token_list:
                continue
            if i == '+':
                n = node(token("name", "__add"))
                tok = []
                for i in range(index):
                    tok.append(tokens[i])
                n.append(self.expr(tok, False))
                tok = []
                for i in range(index+1, len(tokens)):
                    tok.append(tokens[i])
                n.append(self.expr(tok, False))
                return node(token("name", "call"), n)
            if i == '-':
                n = node(token("name", "__sub"))
                tok = []
                for i in range(index):
                    tok.append(tokens[i])
                n.append(self.expr(tok, False))
                tok = []
                for i in range(index+1, len(tokens)):
                    tok.append(tokens[i])
                n.append(self.expr(tok, False))
                return node(token("name", "call"), n)
        else:
            rev = False
        index = -1
        if not rev:
            tokens.reverse()
        for i in tokens: # operators * and /
            index += 1
            if index == 0 and i == '*':
                continue
            if type(i) == token_list:
                continue
            if i == '*':
                n = node(token("name", "__mul"))
                tok = []
                for i in range(index):
                    tok.append(tokens[i])
                n.append(self.expr(tok, True))
                tok = []
                for i in range(index+1, len(tokens)):
                    tok.append(tokens[i])
                n.append(self.expr(tok, True))
                return node(token("name", "call"), n)
            if i == '/':
                n = node(token("name", "__div"))
                tok = []
                for i in range(index):
                    tok.append(tokens[i])
                n.append(self.expr(tok, True))
                tok = []
                for i in range(index+1, len(tokens)):
                    tok.append(tokens[i])
                n.append(self.expr(tok, True))
                return node(token("name", "call"), n)
        else:
            return self.factor(tokens)
        

    def factor(self, tokens):
        if len(tokens) == 0:
            return node(token("name", "null"))
        if len(tokens) == 2:
                if type(tokens[0]) == token:
                    if tokens[0].type == 'name':
                        if tokens[0] == 'sizeof':
                            return node(token("name", "call"), node(tokens[0], self.expr(tokens[1].e)))
                        if type(tokens[1]) == token_list:
                            if tokens[1].sig == 0:
                                n = node(token("name", "call"), node(tokens[0]))
                                buf = []
                                expr = []
                                for i in tokens[1]:
                                    if i == ',':
                                        expr.append(buf)
                                        buf = []
                                        continue
                                    buf.append(i)
                                if buf != []:
                                    expr.append(buf)
                                for i in expr:
                                    n.child[0].append(self.expr(i))
                                
                                return n


                    if tokens[0] == '*':
                        return node(token("name", "call"), node(token("name", "__naming"), node(tokens[1])))
                    if tokens[0] == '&':
                        return node(token("name", "call"), node(token("name", "__addres"), node(tokens[1])))
                    
        if type(tokens[0]) == token_list:
            if len(tokens) == 2:
                if tokens[0].sig == 0:
                    if type(tokens[-1]) == token:
                        if tokens[-1].type == "name" and tokens[-1].type == "number":
                            return node(token("name", "convert"), node(tokens[1]), self.type(tokens[0].e))
            if len(tokens) == 1:
                return self.expr(tokens[0].e)
            return self.expr(tokens[0].e)
        return node(tokens[0])