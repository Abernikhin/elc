class preproc:
    def __init__(self, string: str):
        self.code = string
    
    def include(self):
        result = ""
        lines = self.code.split('\n')
        for i in lines:
            if len(i) > 0:
                if i[0] == '#':
                    command = i.split(' ')
                    if command[0] == "#using":
                        with open(command[1], 'r')as f:
                            result += f.read()+'\n'
                        continue
            result += i
        self.code = result

    def define(self):
        result = ""
        lines = self.code.split('\n')
        consts = []
        for i in lines:
            print(i)
            print(consts)
            if len(i) > 0:
                if i[0] == '#':
                    command = i.split(' ', 2)
                    if command[0] == "#define":
                        print(command)
                        consts.append([command[1], command[2]])
                        continue
                else:
                    buf = ""
                    b = []
                    for a in i:
                        if a in [' ', ',', '(', ')', '[', ']', '{', '}', ';', ':', '=']:
                            b.append(buf)
                            b.append(a)
                            buf = ""
                            continue
                        buf += a
                    for a in b:
                        for c in consts:
                            if a == c[0]:
                                result += c[1]
                                break
                        else:
                            result += 1
        self.code = result

    def __call__(self):
        self.include()
        return self.code