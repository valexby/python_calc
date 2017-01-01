#!/usr/bin/env python

import sys, pdb, unittest, math

class Number():

    def __init__(self, number):
        self.__number__ = number

    def interpret(self):
        return self.__number__

class MathFunction():
    argc = 1
    def __init__(self, argv):
        self.__argv__ = argv

class BinaryOperator(MathFunction):
    argc = 2

class Plus(BinaryOperator):
    def interpret(self):
        return self.__argv__[0].interpret() + self.__argv__[1].interpret()

class Mul(BinaryOperator):
    def interpret(self):
        return self.__argv__[0].interpret() * self.__argv__[1].interpret()

class Minus(BinaryOperator):
    def interpret(self):
        return self.__argv__[0].interpret() - self.__argv__[1].interpret()


class Divide(BinaryOperator):
    def interpret(self):
        return self.__argv__[0].interpret() / self.__argv__[1].interpret()

class DivideCarry(BinaryOperator):
    def interpret(self):
        return self.__argv__[0].interpret() % self.__argv__[1].interpret()

class DivideModule(BinaryOperator):
    def interpret(self):
        return self.__argv__[0].interpret() // self.__argv__[1].interpret()

class Power(BinaryOperator):
    def interpret(self):
        return self.__argv__[0].interpret() ** self.__argv__[1].interpret()

class Absolute(MathFunction):
    def interpret(self):
        return abs(self.__argv__[0].interpret())

class Inverse(MathFunction):
    def interpret(self):
        return  0 - self.__argv__[0].interpret()

class Sqrt(MathFunction):
    def interpret(self):
        return  math.sqrt(self.__argv__[0].interpret())

class Log(MathFunction):
    def interpret(self):
        return  math.log(self.__argv__[0].interpret())

class Log10(MathFunction):
    def interpret(self):
        return  math.log10(self.__argv__[0].interpret())

class Cos(MathFunction):
    def interpret(self):
        return  math.cos(self.__argv__[0].interpret())

class Sin(MathFunction):
    def interpret(self):
        return  math.sin(self.__argv__[0].interpret())

class Acos(MathFunction):
    def interpret(self):
        return  math.acos(self.__argv__[0].interpret())

class Asin(MathFunction):
    def interpret(self):
        return  math.asin(self.__argv__[0].interpret())

class Hypot(BinaryOperator):
     def interpret(self):
        return  math.hypot(self.__argv__[0].interpret(), self.__argv__[1].interpret())

class Atan(MathFunction):
    def interpret(self):
        return  math.atan(self.__argv__[0].interpret())

class Atan2(BinaryOperator):
    def interpret(self):
        return  math.atan2(self.__argv__[0].interpret(), self.__argv__[1].interpret())

class UnknownSyntaxException(Exception):
    pass

class Stack():

    def __init__(self):
        self.__data__ = []

    def push(self, nooby):
        self.__data__.append(nooby)

    def get(self):
        if len(self.__data__) == 0:
            return None
        return self.__data__[-1]

    def pop(self, num = 0):
        if len(self.__data__) < num:
            return None
        if num == 0:
            out = self.__data__[-1]
            num = 1
        else:
            out = self.__data__[-(num):]
        self.__data__ = self.__data__[:-(num)]
        return out

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
        with self.assertRaises(ZeroDivisionError):
            calc("5 / 0 + 4")

    def test_inversion(self):
        self.assertEqual(calc("2 ^ -1 + (-3 + 2)"), -0.5)

    def test_power(self):
        self.assertEqual(calc("2 ^ 2"), 4)
        self.assertEqual(calc("2 ^ -1"), 0.5)
        self.assertEqual(calc("16 ^ 0.25"), 2)

    def test_sqrt(self):
        self.assertEqual(calc("sqrt(4.5)"), math.sqrt(4.5))
        self.assertEqual(calc("sqrt(4)"), 2)

    def test_log(self):
        self.assertEqual(calc("log10(10^5)"), 5)
        self.assertEqual(calc("log(5)"), math.log(5))

    def test_trigonometry(self):
        self.assertEqual(calc("asin(sin(5)) + acos(cos(5))"), math.asin(math.sin(5)) + 
            math.acos(math.cos(5)))

    def test_hypot(self):
        self.assertEqual(calc("hypot(3, -1)"), math.hypot(3, -1))

    def test_atan(self):
        self.assertEqual(calc("atan(0.3)"), math.atan(0.3))
        self.assertEqual(calc("atan2(4, 2)"), math.atan2(4, 2))

ops_list = {'log':(5, Log), 'log10':(5, Log10), 'abs':(5, Absolute), 'inv':(5, Inverse), 'sqrt':(5, Sqrt),
        'sin':(5, Sin), 'asin':(5, Asin), 'cos':(5, Cos), 'acos':(5, Acos), 'hypot':(5, Hypot),
        'atan':(5, Atan), 'atan2':(5, Atan2),
        '^':(4, Power), 
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
    for i in range(5, 0, -1):
        if source[:i] in ops_list:
            return i
    return 1

def delete_spaces(source):
    return "".join(source.split(' '))
    
def make_machine_handy(source):
    """

    Split string math expression.

    """
    i = 0
    res = []
    source = delete_spaces(source)
    while (i < len(source)):
        if source[i] == '-' and (len(res) == 0 or source[i-1] == ',' or (res[-1] != ')' and not isinstance(res[-1], (int, float)))):
            res.append('inv')
            i += 1
            continue
        if ('0' <= source[i] <= '9' or source[i] == '.'):
            (num, shift) = get_numb(source[i:])
            res.append(num)
            i += shift
            continue
        if (source[i] == 'e'):
            res.append(math.e)
            i += 1
            continue
        op_pos = i + find_operator(source[i:])
        if source[i:op_pos] == '--':
            res.append('+')
        elif ops_list.get(source[i:op_pos]) != None:
            res.append(source[i:op_pos])
        elif source[i:op_pos] != ',':
            raise UnknownSyntaxException()
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
    result = op_class(expr_stack.pop(op_class.argc))
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
    while expr_stack.lenght() != 1 or not op_stack.is_empty():
        make_expression(expr_stack, op_stack)
    return expr_stack.pop()

def calc(soucre):
    tokens = make_machine_handy(soucre)
    expression = make_polish(tokens)
    result = expression.interpret()
    return result

if __name__ == '__main__':
    unittest.main()
