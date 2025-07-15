from parser.node import node, token

class parser:
    def __init__(self, tokens: list[token]) -> None:
        self.tokens = tokens
        self.result = []
    
    def parsing(self):
        while len(self.tokens) > 0:
            for i in range(self.module()):
                self.tokens.pop(0)
        return self.result
    
    def module(self, module: str = '', size = 0):
        if self.tokens[0] == "module":
            if module == '':
                module += '::' + self.tokens[1].lit
            size += 2
            
            tokens = []
            if self.tokens[2] != '{':
                raise RuntimeError("syntax error: exepted '{' after module")
            for i in range(2, len(self.tokens)):
                tokens.append(self.tokens[i])
                if self.tokens[i] == ';':
                    break
            if tokens[-2] != '}':
                raise RuntimeError("syntax error: exepted '}'")
            size += len(tokens)
            tokens.pop()
            if tokens[-1] != ';':
                raise RuntimeError("syntax error: exepted ';' after close module")
            
            n = node(self.tokens[1])
            
            self.result.append(node(self.tokens[0], n))
            
        return size