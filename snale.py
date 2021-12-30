import sys
args = sys.argv

if len(args) < 2:
    print("Not enough arguments!")
    exit(1)
elif len(args) > 2:
    print("Too many arguments!")
    exit(1)
else:
    file = args[1]

def push(arg):
    return ("PUSH", arg)
def drop():
    return ("DROP", )
def clear():
    return ("CLEAR", )
def dup():
    return ("DUP", )
def swap():
    return ("SWAP", )
def over():
    return ("OVER", )
def rot():
    return ("ROT", )
def out():
    return ("OUT", )
def plus():
    return ("PLUS", )
def minus():
    return ("MINUS", )
def mul():
    return ("MUL", )
def div():
    return ("DIV", )
def fdiv():
    return ("FDIV", )
def mod():
    return("MOD", )
def smaller():
    return ("SMALLER", )
def smaller_equal():
    return ("SMALLER_EQUAL", )
def greater():
    return ("GREATER", )
def greater_equal():
    return ("GREATER_EQUAL", )
def equal():
    return ("EQUAL", )
def ifcond():
    return ("IF", )
def elsecond():
    return ("ELSE", )
def whilecond():
    return ("WHILE", )
def end():
    return ("END", )

program = []
stack = []
def split_file(f):
    return [ch for ch in f]
def parse_file(f):
    content = split_file(open(f, "r").read())
    tok = ""
    in_string = False
    for ch in content:
        if ch == '"' and not in_string: in_string = True
        elif ch == '"' and in_string: in_string = False
        
        if in_string and ch != '"': tok += ch
        elif not in_string and ch != '"':
            if ch != '\n' and ch != ' ' and ch != '\t' and ch != '\r':
                tok += ch
            else:
                if tok != '':
                    if tok == "drop": program.append(drop())
                    elif tok == "clr": program.append(clear())
                    elif tok == "dup": program.append(dup())
                    elif tok == "swap": program.append(swap())
                    elif tok == "over": program.append(over())
                    elif tok == "rot": program.append(rot())
                    elif tok == ".": program.append(out())
                    elif tok == "+": program.append(plus())
                    elif tok == "-": program.append(minus())
                    elif tok == "*": program.append(mul())
                    elif tok == "/": program.append(div())
                    elif tok == "f/": program.append(fdiv())
                    elif tok == "%": program.append(mod())
                    elif tok == "<": program.append(smaller())
                    elif tok == "<=": program.append(smaller_equal())
                    elif tok == ">": program.append(greater())
                    elif tok == ">=": program.append(greater_equal())
                    elif tok == "=": program.append(equal())
                    elif tok == "if": program.append(ifcond())
                    elif tok == "else": program.append(elsecond())
                    elif tok == "while": program.append(whilecond())
                    elif tok == "end": program.append(end())
                    else:
                        try: program.append(push(int(tok)))
                        except: program.append(push(str(tok)))

                tok = ""


def simulate(src):
    loop = []
    elseloop = []
    whileloop = []
    conds = 0
    cond_type = None
    cond_started = False
    for tok in src:
        if tok[0] == "PUSH" and not cond_started:
            stack.append(tok[1])
        elif tok[0] == "DROP" and not cond_started:
            stack.pop()
        elif tok[0] == "CLEAR" and not cond_started:
            stack.clear()
        elif tok[0] == "DUP" and not cond_started:
            stack.append(stack[len(stack) - 1])
        elif tok[0] == "SWAP" and not cond_started:
            b = stack.pop()
            a = stack.pop()
            stack.append(b)
            stack.append(a)
        elif tok[0] == "OVER" and not cond_started:
            stack.append(stack[len(stack) - 2])
        elif tok[0] == "ROT" and not cond_started:
            c = stack.pop()
            b = stack.pop()
            a = stack.pop()
            stack.append(b)
            stack.append(c)
            stack.append(a)
        elif tok[0] == "OUT" and not cond_started:
            print(stack[len(stack) - 1])
        elif tok[0] == "PLUS" and not cond_started:
            assert len(stack) >= 2, "Cannot perform plus op on empty value"
            b = stack.pop()
            a = stack.pop()
            stack.append(a + b)
        elif tok[0] == "MINUS" and not cond_started:
            assert len(stack) >= 2, "Cannot perform minus op on empty value"
            b = stack.pop()
            a = stack.pop()
            stack.append(a - b)
        elif tok[0] == "MUL" and not cond_started:
            assert len(stack) >= 2, "Cannot perform mul op on empty value"
            b = stack.pop()
            a = stack.pop()
            stack.append(a * b)
        elif tok[0] == "DIV" and not cond_started:
            assert len(stack) >= 2, "Cannot perform div op on empty value"
            import math
            b = stack.pop()
            assert b != 0, "Cannot divide by 0"
            a = stack.pop()
            stack.append(math.floor(a / b))
        elif tok[0] == "FDIV" and not cond_started:
            assert len(stack) >= 2, "Cannot perform fdiv op on empty value"
            b = stack.pop()
            assert b != 0, "Cannot divide by 0"
            a = stack.pop()
            stack.append(a / b)
        elif tok[0] == "MOD" and not cond_started:
            assert len(stack) >= 2, "Cannot perform mod op on empty value"
            b = stack.pop()
            assert b != 0, "Cannot divide by 0"
            a = stack.pop()
            stack.append(a % b)
        elif tok[0] == "SMALLER" and not cond_started:
            stack.append(tok[0])
        elif tok[0] == "SMALLER_EQUAL" and not cond_started:
            stack.append(tok[0])
        elif tok[0] == "GREATER" and not cond_started:
            stack.append(tok[0])
        elif tok[0] == "GREATER_EQUAL" and not cond_started:
            stack.append(tok[0])
        elif tok[0] == "EQUAL" and not cond_started:
            stack.append(tok[0])
        elif tok[0] == "IF":
            conds += 1
            if not cond_started:
                cond_started = True
                cond_type = "if"
            else:
                if cond_type == "if": loop.append(tok)
                elif cond_type == "else": elseloop.append(tok)
                elif cond_type == "while": whileloop.append(tok)
        elif tok[0] == "ELSE":
            #TODO: REWORK
            conds -= 1
            if conds == 0:
                cond_type = "else"
            else: 
                if cond_started:
                    if cond_type == "if": loop.append(tok)
                    elif cond_type == "else": elseloop.append(tok)
                    elif cond_type == "while": whileloop.append(tok)
            conds += 1
        elif tok[0] == "WHILE":
            conds += 1
            if not cond_started:
                cond_started = True
                cond_type = "while"
            else:
                if cond_type == "if": loop.append(tok)
                elif cond_type == "else": elseloop.append(tok)
                elif cond_type == "while": whileloop.append(tok)
        elif tok[0] == "END":
            conds -= 1
            if conds == 0:
                cond_started = False
                if cond_type != "while":
                    op = stack.pop()
                    if op == "SMALLER":
                        if stack[len(stack) - 2] < stack[len(stack) - 1]: simulate(loop)
                        else: simulate(elseloop)
                    elif op == "SMALLER_EQUAL":
                        if stack[len(stack) - 2] <= stack[len(stack) - 1]: simulate(loop)
                        else: simulate(elseloop)
                    elif op == "GREATER":
                        if stack[len(stack) - 2] > stack[len(stack) - 1]: simulate(loop)
                        else: simulate(elseloop)
                    elif op == "GREATER_EQUAL":
                        if stack[len(stack) - 2] >= stack[len(stack) - 1]: simulate(loop)
                        else: simulate(elseloop)
                    elif op == "EQUAL":
                        if stack[len(stack) - 2] == stack[len(stack) - 1]: simulate(loop)
                        else: simulate(elseloop)
                else:
                    op = stack.pop()
                    if op == "SMALLER":
                        while stack[len(stack) - 2] < stack[len(stack) - 1]: simulate(whileloop)
                    elif op == "SMALLER_EQUAL":
                        while stack[len(stack) - 2] <= stack[len(stack) - 1]: simulate(whileloop)
                    elif op == "GREATER":
                        while stack[len(stack) - 2] > stack[len(stack) - 1]: simulate(whileloop)
                    elif op == "GREATER_EQUAL":
                        while stack[len(stack) - 2] >= stack[len(stack) - 1]: simulate(whileloop)
                    elif op == "EQUAL":
                        while stack[len(stack) - 2] == stack[len(stack) - 1]: simulate(whileloop)
            else:
                if cond_type == "if": loop.append(tok)
                elif cond_type == "else": elseloop.append(tok)
                elif cond_type == "while": whileloop.append(tok)
        # elif tok[0] != "END" and tok[0] != "IF" and tok[0] != "ELSE" and tok[0] != "WHILE" and cond_started:
        else:
            if cond_type == "if": loop.append(tok)
            elif cond_type == "else": elseloop.append(tok)
            elif cond_type == "while": whileloop.append(tok)

parse_file(file)
# print(program)
simulate(program)