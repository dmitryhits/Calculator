import re
from collections import deque


class Operator:
    def __init__(self, operator_string):
        self.op = operator_string
        self.rank = -1
        if operator_string == '+':
            self.rank = 0
            # print(f'rank {self.rank}')
        elif operator_string == '-':
            self.rank = 0
            # print(f'rank {self.rank}')
        elif operator_string == '*':
            self.rank = 1
            # print(f'rank {self.rank}')
        elif operator_string == '/':
            self.rank = 1
            # print(f'rank {self.rank}')

    def __str__(self):
        return str(self.op)

    def __repr__(self):
        return str(self.op)

    def sign(self):
        return str(self.op)

    def get_rank(self):
        return self.rank


def decode_operators(operator_string):
    """If the number of '-' operators is odd then the result is '-' otherwise the result is '+' """
    if ('-' in operator_string and operator_string.count('-') % 2 == 0) or '+' in operator_string:
        op = Operator('+')
        # print(f'operator {op} of rank {op.rank}')
        return op
    elif '-' in operator_string:
        op = Operator('-')
        # print(f'operator {op} of rank {op.rank}')
        return Operator('-')
    elif ('/' in operator_string or '*' in operator_string) and len(operator_string) > 1:
        print('Invalid expression')
        return 'moving on'
    else:
        op = Operator(operator_string)
        # print(f'operator {op} of rank {op.rank}')
        return op


class Calculator:
    def __init__(self):
        self.variables = {}

    def check_variable(self, var_string):
        var_string = var_string.strip()
        if var_string.isalpha():
            return var_string
        else:
            print('Invalid identifier')
            return ''

    def decode_variable(self, variable_string):
        """Returns value of a variable or an empty string in the variable is unknown or invalid"""
        variable_string = variable_string.strip()
        # print(variable_string)
        if variable_string.isalpha() and variable_string in self.variables:
            return self.variables[variable_string]
        elif variable_string.isalpha():
            print('Unknown variable')
            # print(self.variables)
            return 'moving on'
        elif variable_string.startswith('-') or variable_string.isdecimal():
            return int(variable_string)
        else:
            print('Invalid assignment')
            return 'moving on'

    def decode_assignment(self, assign_string):
        if assign_string.count('=') > 1:
            print('invalid assignment')
            return 'moving on'
        name, value = assign_string.split('=')
        key = self.check_variable(name)
        value = self.decode_variable(value)
        if key and value != '':
            self.variables[key] = value
            return 'moving on'
        else:
            return 'moving on'

    def string2infix(self, expression_string):
        """ Takes expression as a string and converts it to list with values, parentheses and operators
        arranged in infix order"""
        operators = '-+*/'
        expressions_list = []

        is_start = True
        is_variable = False
        is_operator = False
        is_parenthesis = False
        for i in expression_string:

            # print(f"'exp list', {list(expressions_list)}")
            # print(f'i: {i}')
            # print(f'i={i}, Start: {is_start}, Variable: {is_variable}, Operator: {is_operator}')
            # at the start of the expression I expect a sign as a part of the variable or a variable
            if is_start and (i in operators or i.isalnum()):
                v = i
                is_variable = True
                is_start = False
            # expression can also start with a parenthesis
            elif is_start and i == '(':
                is_start = False
                is_parenthesis = True
                expressions_list.append(i)
            # variable starting after parenthesis
            elif is_parenthesis and i.isalnum():
                is_variable = True
                is_parenthesis = False
                v = i
            # operator starts after parenthesis
            elif is_parenthesis and i in operators:
                is_operator = True
                is_parenthesis = False
                op = i
            # variable starting after the operator decode operator
            elif i.isalnum() and is_operator:
                # print('variable starting after the operator')
                op_ = decode_operators(op)
                if op_ == 'moving on':
                    return 'moving on'
                else:
                    expressions_list.append(op_)
                is_operator = False
                # start variable
                v = i
                is_variable = True
            # variable starts after parenthesis or space
            elif i.isalnum() and not is_variable:
                v = i
                is_variable = True
            # variable continues
            elif i.isalnum() and is_variable:
                v += i
            # operator starts after variable
            elif i in operators and is_variable:
                op = i
                is_operator = True
                is_variable = False
                v_ = self.decode_variable(v)
                if v_ == 'moving on':
                    return 'moving on'
                else:
                    expressions_list.append(v_)
            # operator continues
            elif i in operators and is_operator:
                op += i
            # ignore spaces
            elif i.isspace():
                continue
            #  simply add left or right parentheses
            elif i == '(' or i == ')':
                is_parenthesis = True
                if is_variable:
                    v_ = self.decode_variable(v)
                    if v_ == 'moving on':
                        return 'moving on'
                    else:
                        expressions_list.append(v_)
                    is_variable = False
                elif is_operator:
                    op_ = decode_operators(op)
                    if op_ == 'moving on':
                        return 'moving on'
                    else:
                        expressions_list.append(op_)
                    is_operator = False
                expressions_list.append(i)
        # variable at the end of the expression
        else:
            if is_variable:
                v_ = self.decode_variable(v)
                if v_ == 'moving on':
                    return 'moving on'
                else:
                    expressions_list.append(v_)
                is_variable = False
            elif is_operator:
                op_ = decode_operators(op)
                if op_ == 'moving on':
                    return 'moving on'
                else:
                    expressions_list.append(op_)
                is_operator = False

        # end of expression
        # print(f'infix list: {expressions_list}')
        return expressions_list

    def infix2postfix(self, infix_list):
        if infix_list == 'moving on':
            return 'moving on'
        # print(f'infix list: {infix_list}')
        result_stack = deque()
        operator_stack = deque()
        for i in infix_list:
            # print(f"op stack: {operator_stack}")
            # print(f'result stack: {result_stack}')
            # print(f'i: {i}')
            # print(f'Element {i} of type {type(i)}')
            # Add operands (numbers and variables) to the result (postfix notation) as they arrive.
            if type(i) == int:
                result_stack.append(i)
            # If the stack is empty or contains a left parenthesis on top, push the incoming operator on the stack.
            elif type(i) == Operator and (len(operator_stack) == 0 or list(operator_stack)[-1] == '('):
                # print(f"1: op {i} with rank {i.get_rank()}")
                operator_stack.append(i)
            # If the incoming operator has higher precedence than the top of the stack, push it on the stack.
            elif type(i) == Operator and i.rank > list(operator_stack)[-1].rank:
                # print(f'2: op {i} with rank {i.get_rank()}')
                operator_stack.append(i)
            # If the precedence of the incoming operator is lower than or equal to that of the top of the stack
            elif type(i) == Operator and i.rank <= list(operator_stack)[-1].rank:
                # print(f'3: op {i} with rank {i.get_rank()}')
                # pop operator stack until you find lower rank operator or left parenthesis
                while len(operator_stack) != 0 \
                        and list(operator_stack)[-1] != '(' \
                        and list(operator_stack)[-1].rank >= i.rank:
                    # add operators to the result

                    result_stack.append(operator_stack.pop())
                # then add the incoming operator to the stack.
                operator_stack.append(i)
            # If the incoming element is a left parenthesis, push it on the stack.
            elif i == '(':
                operator_stack.append(i)
            # If the incoming element is a right parenthesis,
            elif i == ')':
                # pop operator stack until you find left parenthesis
                while operator_stack:
                    # print(operator_stack)
                    # after finding the left parenthesis pop and discard it
                    if list(operator_stack)[-1] == '(':
                        operator_stack.pop()
                        break
                    # others append to result stack
                    result_stack.append(operator_stack.pop())
                    # print(bool(operator_stack))
                # if no left parenthesis found then the expression is invalid
                else:
                    print('Invalid expression')
                    return 'moving on'

        # At the end of the expression, pop the stack and add all operators to the result.
        while operator_stack:
            op = operator_stack.pop()
            if op != '(':
                result_stack.append(op)
            else:
                print('Invalid expression')
                return 'moving on'
        return result_stack

    def solve_postfix(self, postfix_stack):
        if postfix_stack == 'moving on':
            return 'moving on'
        # ('postfix lst:',  list(postfix_stack))
        result_stack = deque()
        for i in postfix_stack:
            # print(f'result stack: {result_stack}')
            if type(i) == int:
                result_stack.append(i)
            else:
                b = result_stack.pop()
                a = result_stack.pop()
                # print(f'r = {a} {i.sign()} {b}')
                if i.sign() == '/':
                    r = a // b
                elif i.sign() == '*':
                    r = a * b
                    # print('r', r)
                elif i.sign() == '-':
                    r = a - b
                elif i.sign() == '+':
                    r = a + b
                    # print('r', r)
                result_stack.append(r)
        return result_stack.pop()

    def decode_string(self, in_string):
        # commands start with '/'
        if in_string.startswith('/'):
            return self.decode_command(in_string)
        # assignments have an '=' sign in them
        elif '=' in in_string:
            return self.decode_assignment(in_string)
        # ignore empty strings
        elif in_string == '':
            return 'moving on'
        # everything else is probably and expression that should be evaluated
        else:
            try:
                infix_list = self.string2infix(in_string)
                postfix_list = self.infix2postfix(infix_list)
                answer = self.solve_postfix(postfix_list)
                return answer
            except ValueError:
                print('Invalid expression')
                return 'moving on'

    def decode_command(self, command_string):
        if command_string == '/exit':
            print('Bye')
            return 'exit'
        elif command_string == '/help':
            print('The program calculates the inputted expression of numbers')
            return 'moving on'
        else:
            print('Unknown command')
            return 'moving on'


if __name__ == '__main__':
    calc = Calculator()
    while True:
        answer = calc.decode_string(input())
        if answer == 'exit':
            break
        elif answer == 'moving on':
            continue
        else:
            print(answer)

