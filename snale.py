import sys
import codecs

if len(sys.argv) < 2:
    print("Not enough arguments!")
    exit(1)
elif len(sys.argv) > 2:
    print("Too many arguments!")
    exit(1)
else:
    file = sys.argv[1]

def push(arg):
    return ("PUSH", arg)
def drop():
    return ("DROP", )
def clear():
    return ("CLEAR", )
def const():
    return ("CONST", )
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
def new_line():
    return ("NEWLINE", )
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
def macro_is():
    return ("IS", )
def endef():
    return ("ENDEF", )
def call():
    return ("CALL", )
def end():
    return ("END", )
program = []
stack = []
const_names = []
const_vals = []
macros_name = []
macros_body = []

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
                    elif tok == "const": program.append(const())
                    elif tok == "dup": program.append(dup())
                    elif tok == "swap": program.append(swap())
                    elif tok == "over": program.append(over())
                    elif tok == "rot": program.append(rot())
                    elif tok == ".": program.append(out())
                    elif tok == "nl": program.append(new_line())
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
                    elif tok == "is": program.append(macro_is())
                    elif tok == "endef": program.append(endef())
                    elif tok == "call": program.append(call())
                    elif tok == "end": program.append(end())
                    else:
                        try: program.append(push(int(tok)))
                        except: program.append(push(str(tok)))

                tok = ""


def simulate(src):
    loop = []
    elseloop = []
    whileloop = []
    macro = []
    conds = 0
    cond_type = None
    cond_started = False
    for _, tok in enumerate(src):
        if tok[0] == "PUSH" and not cond_started:
            if cond_type != "macro":
                if tok[1] not in const_names:
                    stack.append(tok[1])
                else:
                    stack.append(const_vals[const_names.index(tok[1])])
            else:
                macro.append(tok)
        elif tok[0] == "DROP" and not cond_started:
            if cond_type != "macro":
                stack.pop()
            else:
                macro.append(tok)
        elif tok[0] == "CLEAR" and not cond_started:
            if cond_type != "macro":
                stack.clear()
            else:
                macro.append(tok)
        elif tok[0] == "CONST" and not cond_started:
            if cond_type != "macro":
                val = stack.pop()
                definition = stack.pop()
                const_names.append(definition)
                const_vals.append(val)
            else:
                macro.append(tok)
        elif tok[0] == "DUP" and not cond_started:
            if cond_type != "macro":
                stack.append(stack[len(stack) - 1])
            else:
                macro.append(tok)
        elif tok[0] == "SWAP" and not cond_started:
            if cond_type != "macro":
                b = stack.pop()
                a = stack.pop()
                stack.append(b)
                stack.append(a)
            else:
                macro.append(tok)
        elif tok[0] == "OVER" and not cond_started:
            if cond_type != "macro":
                stack.append(stack[len(stack) - 2])
            else:
                macro.append(tok)
        elif tok[0] == "ROT" and not cond_started:
            if cond_type != "macro":
                c = stack.pop()
                b = stack.pop()
                a = stack.pop()
                stack.append(b)
                stack.append(c)
                stack.append(a)
            else:
                macro.append(tok)
        elif tok[0] == "OUT" and not cond_started:
            if cond_type != "macro":
                if type(stack[len(stack) - 1]) == int: print(stack.pop(), end='')
                else: print(codecs.decode(stack.pop(), 'unicode_escape'), end='')
            else:
                macro.append(tok)
        elif tok[0] == "NEWLINE" and not cond_started:
            if cond_type != "macro":
                print()
            else:
                macro.append(tok)
        elif tok[0] == "PLUS" and not cond_started:
            if cond_type != "macro":
                assert len(stack) >= 2, "Cannot perform plus op on empty value"
                b = stack.pop()
                a = stack.pop()
                stack.append(a + b)
            else:
                macro.append(tok)
        elif tok[0] == "MINUS" and not cond_started:
            if cond_type != "macro":
                assert len(stack) >= 2, "Cannot perform minus op on empty value"
                b = stack.pop()
                a = stack.pop()
                stack.append(a - b)
            else:
                macro.append(tok)
        elif tok[0] == "MUL" and not cond_started:
            if cond_type != "macro":
                assert len(stack) >= 2, "Cannot perform mul op on empty value"
                b = stack.pop()
                a = stack.pop()
                stack.append(a * b)
            else:
                macro.append(tok)
        elif tok[0] == "DIV" and not cond_started:
            if cond_type != "macro":
                assert len(stack) >= 2, "Cannot perform div op on empty value"
                import math
                b = stack.pop()
                assert b != 0, "Cannot divide by 0"
                a = stack.pop()
                stack.append(math.floor(a / b))
            else:
                macro.append(tok)
        elif tok[0] == "FDIV" and not cond_started:
            if cond_type != "macro":
                assert len(stack) >= 2, "Cannot perform fdiv op on empty value"
                b = stack.pop()
                assert b != 0, "Cannot divide by 0"
                a = stack.pop()
                stack.append(a / b)
            else:
                macro.append(tok)
        elif tok[0] == "MOD" and not cond_started:
            if cond_type != "macro":
                assert len(stack) >= 2, "Cannot perform mod op on empty value"
                b = stack.pop()
                assert b != 0, "Cannot divide by 0"
                a = stack.pop()
                stack.append(a % b)
            else:
                macro.append(tok)
        elif tok[0] == "SMALLER" and not cond_started:
            if cond_type != "macro":
                stack.append(tok[0])
            else:
                macro.append(tok)
        elif tok[0] == "SMALLER_EQUAL" and not cond_started:
            if cond_type != "macro":
                stack.append(tok[0])
            else:
                macro.append(tok)
        elif tok[0] == "GREATER" and not cond_started:
            if cond_type != "macro":
                stack.append(tok[0])
            else:
                macro.append(tok)
        elif tok[0] == "GREATER_EQUAL" and not cond_started:
            if cond_type != "macro":
                stack.append(tok[0])
            else:
                macro.append(tok)
        elif tok[0] == "EQUAL" and not cond_started:
            if cond_type != "macro":
                stack.append(tok[0])
            else:
                macro.append(tok)
        elif tok[0] == "IF":
            if cond_type != "macro":
                conds += 1
                if not cond_started:
                    cond_started = True
                    cond_type = "if"
                else:
                    if cond_type == "if": loop.append(tok)
                    elif cond_type == "else": elseloop.append(tok)
                    elif cond_type == "while": whileloop.append(tok)
            else:
                macro.append(tok)
        elif tok[0] == "ELSE":
            if cond_type != "macro":
                conds -= 1
                if conds == 0:
                    cond_type = "else"
                else: 
                    if cond_started:
                        if cond_type == "if": loop.append(tok)
                        elif cond_type == "else": elseloop.append(tok)
                        elif cond_type == "while": whileloop.append(tok)
                conds += 1
            else:
                macro.append(tok)
        elif tok[0] == "WHILE":
            if cond_type != "macro":
                conds += 1
                if not cond_started:
                    cond_started = True
                    cond_type = "while"
                else:
                    if cond_type == "if": loop.append(tok)
                    elif cond_type == "else": elseloop.append(tok)
                    elif cond_type == "while": whileloop.append(tok)
            else:
                macro.append(tok)
        elif tok[0] == "IS":
            macros_name.append(stack.pop())
            cond_type = "macro"
        elif tok[0] == "ENDEF":
            cond_type = None
            macros_body.append(macro)
            macro = []
        elif tok[0] == "CALL":
            f = stack.pop()
            if f in macros_name: simulate(macros_body[macros_name.index(f)])
        elif tok[0] == "END":
            if cond_type != "macro":
                conds -= 1
                if conds == 0:
                    cond_started = False
                    if cond_type == "if" or cond_type == "else":
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
                    elif cond_type == "while":
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
            else:
                macro.append(tok)
        else:
            if cond_type == "if": loop.append(tok)
            elif cond_type == "else": elseloop.append(tok)
            elif cond_type == "while": whileloop.append(tok)

parse_file(file)
simulate(program)