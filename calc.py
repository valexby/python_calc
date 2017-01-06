#!/usr/bin/env python

import sys, pdb, unittest, math, re

class Number():

    def __init__(self, number):
        self.__number__ = number

    def interpret(self):
        return self.__number__

class MathFunction():
    argc = 1
    def __init__(self, argv):
        if argv == None:
            raise UnknownSyntaxException("Operator {} needs more arguments".format(type(self)))
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
        self.assertEqual(calc("3sin(3+1)2+(2)(3)+3(3+2)+(1+3)4"), 3*math.sin(3+1)*2+(2)*(3)+3*(3+2)+(1+3)*4)

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
        self.assertEqual(calc("-2 ^ -2"), -0.25)

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

    def test_wrong_operation(self):
        with self.assertRaises(UnknownSyntaxException):
            calc("5 + 2 - ")
            calc("5 + 3 = 8")

ops_list = {'log':(6, Log), 'log10':(6, Log10), 'abs':(6, Absolute), 'sqrt':(6, Sqrt),
        'sin':(6, Sin), 'asin':(6, Asin), 'cos':(6, Cos), 'acos':(6, Acos), 'hypot':(6, Hypot),
        'atan':(6, Atan), 'atan2':(6, Atan2),
        '^':(5, Power), 
        'inv':(4, Inverse), 
        '*':(3, Mul), '/':(3, Divide), '//':(3, DivideModule), '%':(3, DivideCarry),
        '+':(2, Plus), '-':(2, Minus),
        '--':-1, '(':(0, '('), ')':(10, ')')}

def fix_not_explicit_mul(source):
    p = re.compile("((\d|\))(log10|log|abs|sqrt|sin|asin|cos|acos|hypot|atan2|atan|\())|(\)\d)")
    start = 0
    scan = p.scanner(source)
    token = scan.search()
    res = ""
    while token != None:
        end = token.start()
        if (source[end-4:end+1] != 'atan2' and source[end-4:end+1] != 'log10'):
            res += source[start:end+1] + '*';
            start = end+1
        token = scan.search()
    return res + source[start:]

def make_machine_handy(source):
    """

    Splits string expression.

    """
    p = re.compile("(log10|log|abs|sqrt|sin|asin|cos|acos|hypot|atan2|atan|\^|\*|//|/|\%|\+|--|-|,|\(|\))|(\d*\.\d+)|(\d+)")
    scan = p.scanner(source)
    token = scan.search()
    res = []
    while token != None:
        if token.group(1) != None: # operator  
            if token.group(1) == '-' and (len(res) == 0 or (res[-1] != ')' and not isinstance(res[-1], (int, float)))):
                res.append('inv')
            else:
                res.append(token.group(1))
        elif token.group(2) != None: # float  
            res.append(float(token.group(2)))
        else: # integer  
            res.append(int(token.group(3)))
        token = scan.search()
    return [x for x in res if x != ',']

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
    elif token == '(' or op_stack.is_empty() or op_stack.get()[0] < cur_operator[0] or (token == 'inv' and op_stack.get()[1] == Power):
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

def calc(source):
    fixed = fix_not_explicit_mul(source)
    tokens = make_machine_handy(fixed)
    expression = make_polish(tokens)
    result = expression.interpret()
    return result

if __name__ == '__main__':
    unittest.main()
