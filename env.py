import math
from fractions import Fraction

class Environment:
    def __init__(self):
        self.variables = {
                    'T': True,
                    'NIL': None
        };
        self.functions = {
                    '+': self.add,
                    '-': self.subtract,
                    '*': self.multiply,
                    '/': self.divide,
                    '>': self.greater_than,
                    '<': self.less_than,
                    '=': self.equals,
                    '!=': self.not_equal,
                    'and': self.and_operator,
                    'or': self.or_operator,
                    'not': self.not_operator,
                    'car': self.car,
                    'cdr': self.cdr,
                    'cons': self.cons,
                    'sqrt': self.sqrt,
                    'pow': self.power,
                    'define': self.define,
                    'if': self.if_cond,
                    'set!': self.set,
                    'defun': self.defun,
                    'mapcar': self.mapcar
                }
        
    # Evaluates a given expression in the current environment.
    # Handles variables, quoted expressions, and function calls.
    # Returns the evaluated result of the expression.
    def evaluate_expression(self, expression):
        if isinstance(expression, list):
            element = str(expression[0])  # Convert the first element to string

            # Check if the first element is a variable and return its value
            if element in self.variables:
                return self.variables[element]
            
            # Check for 'quote' expression
            if element == 'quote':
                if len(expression) != 2:
                    raise SyntaxError("Malformed quote expression")
                return expression[1]  # Return the quoted value directly
            
            # Check if the first element is a valid function name
            if not isinstance(expression[0], str):
                raise SyntaxError(f"Invalid function call: {expression}")

            # Evaluate a function call by passing the expression to a separate method
            # This will handle looking up the function and applying the operands
            return self.evaluate_function_call(expression)
        
        else:
            # If it's not a list, check if it's a variable or return the value
            if expression in self.variables:
                return self.variables[expression]
            return expression

    # Evaluates a function call expression, which includes:
    # - Checking if the operator is valid (function name).
    # - Handling special operators like 'set!' (variable assignment) and 'defun' (function definition).
    # - Evaluating the operands and passing them to the corresponding function in the environment.
    # Returns the result of the evaluated function call.
    def evaluate_function_call(self, expression):
        # Extract the operator (function name) and operands (arguments) from the expression
        operator, operands = expression[0], expression[1:]

        # Check if the operator (function name) is a known function
        if operator not in self.functions:
            raise NameError(f"Unknown function: {operator}")
        
        # Special handling for 'set!' operator: Assigns a new value to an existing variable
        if operator == 'set!':
            if len(operands) != 2:
                raise SyntaxError("set! requires exactly 2 arguments")
            return self.set(operands[0], self.evaluate_expression(operands[1]))
        
        # Special handling for 'defun' operator: Defines a new function
        if operator == 'defun':
            return self.functions[operator](*operands)
        
        # Special handling for 'mapcar'
        if operator == 'mapcar':
            if len(operands) < 2:
                raise SyntaxError("mapcar requires at least one function and one list argument")
            
            # Evaluate the function but keep the lists unchanged
            func = self.evaluate_expression(operands[0])
            lists = [self.evaluate_expression(lst) for lst in operands[1:]]

            # Ensure all operands after the function are lists
            if not all(isinstance(lst, list) for lst in lists):
                raise TypeError("mapcar requires all arguments after the function to be lists")

            return self.mapcar(func, *lists)

        # Evaluate operands and pass them to the function
        evaluated_operands = [self.evaluate_expression(operand) for operand in operands]
        
        # Call the function (retrieved from the functions dictionary) with the evaluated operands and return the result
        return self.functions[operator](*evaluated_operands)

    # Ensures the value fits within the 32-bit signed integer range
    def check_32bit(self, value):
        INT_MIN = -2_147_483_648
        INT_MAX = 2_147_483_647
        if value < INT_MIN or value > INT_MAX:
            raise OverflowError(f"Integer overflow: {value}")
        return value
    

    # Mathematical operations
    def add(self, *args):
        result = sum(args)
        return self.check_32bit(result)
    
    def subtract(self, a, b):
        result = a - b
        return self.check_32bit(result)
    
    def multiply(self, *args):
        result = 1
        for arg in args:
            result *= arg
            self.check_32bit(result)  # Check for overflow at each step
        return result

    def divide(self, a, b):
        if b == 0:
            raise ZeroDivisionError("Division by zero is not allowed")
        result = Fraction(a, b)
        return self.check_32bit(result)
    
    def sqrt(self, a):
        if a < 0:
            raise ValueError("Cannot compute square root of a negative number")
        result = int(math.sqrt(a))
        return self.check_32bit(result)
    
    def power(self, a, b):
        result = a ** b
        return self.check_32bit(result)


    # Comparison operations
    def greater_than(self, a, b):
        return a > b

    def less_than(self, a, b):
        return a < b

    def equals(self, a, b):
        return a == b
    
    def not_equal(self, a, b):
        return a != b


    # Logical operations
    def and_operator(self, a, b):
        return a and b

    def or_operator(self, a, b):
        return a or b

    def not_operator(self, a):
        return not a


    # List operations
    def car(self, a):
        if isinstance(a, list):
            if a == []:
                return None
            return a[0]
        else:
            return a
        
    def cdr(self, a):
        if isinstance(a, list):
            if a == []:
                return None
            return a[1:]
        else:
            raise SyntaxError("Argument for cdr is not a list")
        
    def cons(self, a, b):
        if a == []:
            a = None
        if b == []:
            b = None

        if a is None and b is None:
            return None  # Equivalent to '() in Lisp'

        if isinstance(b, list):
            return [a] + b  # Creates a new list instead of modifying b

        return [a, '.', b]  # Equivalent to (a . b) in Lisp


    # Environment and State Management operations
    def define(self, var_name, value):
        if not isinstance(var_name, str):
            raise TypeError("Variable name must be a string")
        self.variables[var_name] = value
        return var_name
    
    def if_cond(self, condition, conseq, alt):
        if condition is True:
            return conseq
        else:
            return alt

    def set(self, var_name, value):
        if not isinstance(var_name, str):
            raise SyntaxError(f"set! requires a variable name, got {var_name}")

        if var_name not in self.variables:
            raise NameError(f"Variable '{var_name}' is not defined")

        self.variables[var_name] = value  # Modify the stored variable
        return var_name  # Return variable name for confirmation
    
    def defun(self, name, params, body):
        # Ensure the function name is a valid symbol (string)
        if not isinstance(name, str):
            raise SyntaxError("Function name must be a symbol")

        # Ensure parameters are provided as a list
        if not isinstance(params, list):
            raise SyntaxError("Function parameters must be a list")

        # Define the user function that will be called later. Uses static scoping
        def user_function(*args):
            # Ensure the correct number of arguments are passed to the function
            if len(args) != len(params):
                raise TypeError(f"Function '{name}' expects {len(params)} arguments, got {len(args)}")

            # Create a new environment for this function call
            local_env = Environment()
            local_env.variables = self.variables.copy()  # Copy the current environment's variables
            local_env.functions = self.functions  # Preserve existing function definitions

            # Bind the arguments to the function parameters in the new environment
            for param, arg in zip(params, args):
                local_env.variables[param] = arg

            # Evaluate function body within this new environment
            return local_env.evaluate_expression(body)

        # Save function in the environment
        self.functions[name] = user_function
        return name
    
    # Applies the given function across multiple lists, returning a new list of results.
    def mapcar(self, func, *lists):
        # Combines list into one iterable of tuples. These tuples serve as the arguments to be passed to the specified function
        zipped_list = list(zip(*lists))
        return [self.functions[func](*values) for values in zipped_list]
