#!/usr/bin/env python

import sys, pdb

ops_list = ['+', '-', '*', '/', '**', '//', 'log', 'abs', '(', ')']

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

def find_operator(source):
    for i in range(3, 0, -1):
        if source[:i] in ops_list:
            return i
    return 1

def delete_spaces(source):
    return "".join(source.split(' '))
    
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
        #make negatives machine-like: from '-3' to '(0 - 3)'
        if source[i] == '-' and (len(res) == 0 or (res[-1] != ')' and not isinstance(res[-1], (int, float)))):
            res.extend([0, source[i]])
            i += 1
            continue
        if ('0' < source[i] < '9'):
            shift = get_numb_pos(source[i:])
            res.append(int(source[i:shift + i]))
            i += shift
            continue
        op_pos = i + find_operator(source[i:])
        res.append(source[i:op_pos])
        i = op_pos
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
