import os
import sys
import time
import bdb
from preproc.preproc import*
from lexer.lexer import*
from parser.parser import*
from symantic.analiz import*
from ganare.python import*

def main(flags = []):
    t1 = time.time()
    try:
        out = "out.t"
        mode = "code"
        with open(flags[0], 'r')as f:
            temp1 = f.read()
        etap1 = preproc(temp1)
        temp2 = etap1() # preprocessing code
        etap2 = lexer(temp2)
        temp3 = etap2() # tokinaze
        etap3 = parser(temp3)
        temp4 = etap3() # parsing
        etap4 = analizer(temp4)
        temp4 = etap4()
        temp3 = etap4.ast
        temp5 = ""
        for i in flags:
            if i[0] == '-o':
                out = i[1]
                continue
            if i[0] == '-t':
                if i[1] == "py":
                    mode = 'py'
                continue
            if i[0] == '-i':
                if i[1] == 'tokens':
                    for i in temp2:
                        print(i)
                    continue
                if i[1] == 'ast':
                    for i in temp3:
                        i.info()
                    continue
                if i[1] == 'char':
                    for i in etap4.char.vars:
                        print(i)
                    continue
        if mode == "py":
            etap5 = gc()
            temp5 = etap5.ganare(temp3, temp4)
        with open(out, 'w')as f:
            f.write(temp5)
        
    except KeyboardInterrupt:
        t2 = time.time()
        for i in etap3.tokens: # type: ignore
            print(i)
        print(f"dump[3 in {t2-t1}]")
        return 1
    except RuntimeError:
        t2 = time.time()
        print(f"dump[1 in {t2-t1}]")
        return 1
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