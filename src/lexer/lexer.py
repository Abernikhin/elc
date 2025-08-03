import re
from lexer.token import token

class wrong_token_error(Exception):
    pass

class lexer():
    def __init__(self, source: str) -> None:
        self.code: str = source
        self.rules: dict[str, str] = {
            "skip": r"(\s+)",
            "ignore": r"//([.\\ ]*)",
            "float": r"(\d+\.\d+)",
            "number": r"([123456789]\d+)",
            "char": r"('.'|'\n')",
            "string": r"(\"[.\n]+\")",
            "name": r"([\w\_]+[\d\w\_]*)",
            "dot": r"(\.)",
            "open": r"(\()",
            "close": r"(\))",
            "sopen": r"(\[)",
            "sclose": r"(\])",
            "begin": r"(\{)",
            "end": r"(\})",
            "op|": r"(\|)",
            "op>>": r"(>>)",
            "op<<": r"(<<)",
            "op.": r"(\.)",
            "op->": r"(\->)",
            "op==": r"(\=\=)",
            "op!=": r"(\!\=)",
            "op++": r"(\+\+)",
            "op+": r"(\+)",
            "op--": r"(\-\-)",
            "op-": r"(\-)",
            "op*": r"(\*)",
            "op/": r"(\/)",
            "op&": r"(\&)",
            "op=": r"(\=)",
            "op:": r"(\:)",
            "op,": r"(\,)",
            "op+": r"(\+)",
            "semicolon": r"(\;)",
        }

    def reline(self, obj: str) -> None:
        result = ""
        for i in range(len(obj), len(self.code)):
            result += self.code[i]
        
        self.code = result

    def __call__(self) -> list[token]:
        result: list[token] = []
        while 0 < len(self.code):
            for i in self.rules:
                mo = re.match(self.rules[i], self.code)
                if mo:
                    if i != "skip" and i != "ignore":
                        result.append(token(i, mo.group(1)))
                        self.reline(mo.group(0))
                        break
                    else:
                        self.reline(mo.group(0))
                        break
            else:
                raise wrong_token_error(self.code[0])
        return result
