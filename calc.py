#!/usr/bin/env python

import sys

operators_list = ['+', '-', '*', '/', 'log']

def main():
    polish = make_polish('(1+2)/3')
    print(polish)
    [res] = execute_polish(polish)
    print(res)

def get_numb_pos(string):
    out = 0
    for i in string:
        if ('0' <= i <= '9'): out += 1
        else: break
    return out

def cut_enrty(source):
    if (source[:3] == 'log' or source[:3] == "abs"): 
        return 3

def delete_double_minuses(source):
    ls = source.split('-')
    res = ls[0]
    ls = ls[1:]
    while (len(ls) > 1):
        if (ls[0] == ''):
            res += '+' + ls[1]
            ls = ls[2:]
        else:
            res += '-' + ls[0]
            ls = ls[1:]
    if (len(ls) == 1):
        res += '-' + ls[0]
    return res

#splits string expression on math signs
def make_machine_handy(source):
    i = 0
    res = []
    while (i < len(source)):
        #make negatives machine like: from '-3' to '(0 - 3)'
        if source[i] == '-' and (len(res) == 0 or (res[-1] != ')' and not isinstance(res[-1], (int, float)))):
            res.extend([0, source[i]])
            i += 1
            continue
        if (source[i] == '*' or source[i] == '/') and res[-1] == source[i]:
            res[-1] = source[i]*2
            i+=1
            continue
        if ('0' < source[i] < '9'):
            shift = get_numb_pos(source[i:])
            res.append(int(source[i:shift + i]))
            i += shift
            continue
        res.append(source[i])
        i += 1
    return res

def make_polish(expr):
    stack = "" 
    result = [] 
    while (expr != ""):
        pos = get_numb_pos(expr)
        if pos != 0:
            result.append(int(expr[: pos]))
            expr = expr[pos :]
        elif expr[0] == ')':
            while stack[-1:] != '(' and stack != "":
                result.append(stack[-1:])
                stack = stack[:-1]
            stack = stack[:-1]
            expr = expr[1:]
        else:
            stack += expr[0]
            expr = expr[1:]
        print("-"*20, "\nexpr: ",  expr, "\nstack: ", stack, "\nresult: ", result)
    result.extend(stack[::-1])        
    return result

def execute(a, b, operator):
    if operator == '+':
        return a + b
    elif operator == '-':
        return a - b
    elif operator == '*':
        return a * b
    elif operator == '/':
        return a / b

def execute_polish(expr):
    stack = []
    for i in expr:
        if isinstance(i, int):
            print("-"*20, i, "\nstack: ", stack)
            stack.append(i)
        else:
            print("-"*20, i, "\nstack: ", stack)
            a = stack[-2]
            b = stack[-1]
            stack = stack[:-2]
            stack.append(execute(a, b, i))
    return stack

if __name__ == '__main__':
    sys.exit(main())
