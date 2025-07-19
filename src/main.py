import sys
import time
import bdb
from preproc.preproc import*
from lexer.lexer import*
from parser.parser import*


def main(flags = []):
    t1 = time.time()
    try:
        out = "out.t"
        with open(flags[0], 'r')as f:
            temp1 = f.read()
        etap1 = preproc(temp1)
        temp2 = etap1() # preprocessing code
        etap2 = lexer(temp2)
        temp3 = etap2() # tokinaze
        etap3 = parser(temp3)
        temp4 = etap3() # parsing
        for i in flags:
            if i[0] == '-o':
                out = i[1]
                continue
            if i[0] == '-i':
                if i[1] == 'tokens':
                    for i in temp3:
                        print(i)
                    continue
                if i[1] == 'ast':
                    for i in temp4:
                        i.info()
                    continue
    except bdb.BdbQuit:
        t2 = time.time()
        print(f"dump[2 in {t2-t1}]")
        return 1
    t2 = time.time()
    print(f"dump[0 in {t2-t1}]")

load_falgs = []
load = sys.argv
load.pop(0)
load_falgs.append(load[0])
load.pop(0)
buf = []
for i in load:
    buf.append(i)
    if len(buf) == 2:
        load_falgs.append(buf)
        buf = []

main(load_falgs)