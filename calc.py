#!/usr/bin/env python

import sys, pdb, unittest

class Number():

    def __init__(self, number):
        self.__number__ = number

    def interpret(self):
        return self.__number__

class MathFunction():

    def __init__(self, argument):
        self.__argument__ = argument
    
    @staticmethod
    def is_binary():
        return False

class BinaryOperator():

    def __init__(self, left, right):
        self.__left__ = left
        self.__right__ = right

    @staticmethod
    def is_binary():
        return True

class Plus(BinaryOperator):

    def interpret(self):
        return self.__left__.interpret() + self.__right__.interpret()

class Mul(BinaryOperator):

    def interpret(self):
        return self.__left__.interpret() * self.__right__.interpret()

class Minus(BinaryOperator):

    def interpret(self):
        return self.__left__.interpret() - self.__right__.interpret()

class Divide(BinaryOperator):

    def interpret(self):
        return self.__left__.interpret() / self.__right__.interpret()

class DivideCarry(BinaryOperator):

    def interpret(self):
        return self.__left__.interpret() % self.__right__.interpret()

class DivideModule(BinaryOperator):

    def interpret(self):
        return self.__left__.interpret() // self.__right__.interpret()

class Power(BinaryOperator):

    def interpret(self):
        return self.__left__.interpret() ** self.__right__.interpret()

class Absolute(MathFunction):

    def interpret(self):
        return abs(self.__argument__.interpret())

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

    def get(self):
        if len(self.__data__) == 0:
            return None
        return self.__data__[-1]

    def is_empty(self):
        return self.__data__ == []

    def lenght(self):
        return len(self.__data__)

class TestCalc(unittest.TestCase):

    def test_not_explicit_multiply(self):
        self.assertEqual(calc("(3)(4)"), 12)

    def test_floats(self):
        self.assertEqual(calc("0.3 + 4"), 4.3)

    def test_not_explicit_floats(self):
        self.assertEqual(calc(".3+.4"), 0.7)

    def test_division(self):
        self.assertEqual(calc("5 // 2 + 5 % 2 / 2"), 2.5)

ops_list = {'log':5, 'abs':(5, Absolute),
        '**':(4, Power), 
        '*':(3, Mul), '/':(3, Divide), '//':(3, DivideModule), '%':(3, DivideCarry),
        '+':(2, Plus), '-':(2, Minus),
        '--':-1, '(':(0, '('), ')':(10, ')')}

def get_numb(source):
    length = 0
    for i in source:
        if '0' <= i <= '9' or i == '.': 
            length += 1
        else:
            break
    dummy = source[:length]
    if '.' in dummy:
        num = float(dummy)
    else:
        num = int(dummy)
    return (num, length)

def find_operator(source):
    for i in range(3, 0, -1):
        if source[:i] in ops_list:
            return i
    return 1

def delete_spaces(source):
    return "".join(source.split(' '))
    
def make_machine_handy(source):
    """

    Split string math expression. Substitude negatives like '-3' on '(0 - 3)'.

    """
    i = 0
    res = []
    source = delete_spaces(source)
    while (i < len(source)):
        if source[i] == '-' and (len(res) == 0 or (res[-1] != ')' and not isinstance(res[-1], (int, float)))):
            # Make negatives machine-like: from '-3' to '(0 - 3)'.
            res.extend([0, source[i]])
            i += 1
            continue
        if ('0' <= source[i] <= '9' or source[i] == '.'):
            (num, shift) = get_numb(source[i:])
            res.append(num)
            i += shift
            continue
        op_pos = i + find_operator(source[i:])
        if source[i:op_pos] == '--':
            res.append('+')
        else:
            res.append(source[i:op_pos])
        i = op_pos
    return res

def make_expression(expr_stack, op_stack):
    """

    Make expression from expressions stack tail.
    Swaps arguments for binary operators.

    """
    if op_stack.is_empty():
        # If we have two number without operand betwen them,  
        # we should use multiply. Like (3+1)(4+2)  
        op_class = Mul
    else:
        op_class = op_stack.pop()[1]
    if op_class.is_binary():
        right = expr_stack.pop()
        left = expr_stack.pop()
        result = op_class(left, right)
    else:
        result = op_class(expr_stack.pop())
    expr_stack.push(result)

def handle_token(expr_stack, op_stack, token):
    cur_operator = ops_list.get(token)
    if isinstance(token, (int, float)):
        expr_stack.push(Number(token))
    elif token == ')':
        while op_stack.get()[1] != '(':
            make_expression(expr_stack, op_stack)
        op_stack.pop()
    elif token == '(' or op_stack.is_empty() or op_stack.get()[0] < cur_operator[0]:
        op_stack.push(cur_operator)
    else:
        while not op_stack.is_empty() and cur_operator[0] <= op_stack.get()[0]:
            make_expression(expr_stack, op_stack)
        op_stack.push(cur_operator)

def make_polish(source):
    op_stack = Stack()
    expr_stack = Stack()
    for token in source:
        handle_token(expr_stack, op_stack, token)
    while expr_stack.lenght() != 1:
        make_expression(expr_stack, op_stack)
    return expr_stack.pop()

def calc(soucre):
    tokens = make_machine_handy(soucre)
    expression = make_polish(tokens)
    result = expression.interpret()
    return result

if __name__ == '__main__':
    unittest.main()
