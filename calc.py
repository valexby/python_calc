#!/usr/bin/env python

import sys, pdb

ops_list = {'*':1, '/':1, '//':1, '%':1,
        '--':-1, '(':-1, ')':-1,
        'log':0, 'abs':0,
        '+':2, '-':2,  '**':3}

class Number():
    def __init__(self, number):
        self.__number__ = number

    def interpret(self):
        return self.__number__

class Plus():
    def __init__(self, left, right):
        self.__left__ = left
        self.__right__ = right

    def interpret(self):
        return self.__left__.interpret() + self.__right__.interpret()

class Minus(): 
    def __init__(self, left, right):
        self.__left__ = left
        self.__right__ = right

    def interpret(self):
        return self.__left__.interpret() - self.__right__.interpret()

class Stack():
    def __init__(self):
        self.__data__ = []

    def push(self, nooby):
        self.__data__.append(nooby)

    def pop(self):
        if len(self.__data__) == 0:
            return None
        head = self.__data__[-1]
        self.__data__ = self.__data__[:-1]
        return head

class Evaluator():
    def __init__(self, expression):
        stack = Stack()
        for token in expression:
            if token == '+':
                sub_expression = Plus(stack.pop(), stack.pop())
            elif token == '-':
                sub_expression = Minus(stack.pop(), stack.pop())
            else:
                sub_expression = Number(token)
            stack.push(sub_expression)
        self.__tree__ = stack.pop()

    def interpret(self):
        return self.__tree__.interpret()

def main():
    polish = make_polish('1+2-3')
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
        if source[i:op_pos] == '--':
            res.append('+')
        else:
            res.append(source[i:op_pos])
        i = op_pos
    return res

if __name__ == '__main__':
    sys.exit(main())
