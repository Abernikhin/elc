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

    def __call__(self):
        self.include()
        return self.code