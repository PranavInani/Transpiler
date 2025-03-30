import re

# Add a variable environment
variables = {}

def tokenize(code):
    tokens = re.findall(r'\bif\b|\belse\b|\bfor\b|\d+|[a-zA-Z_][a-zA-Z0-9_]*|[+\-*/=()<>{};]', code)
    return tokens

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self):
        token = self.peek()
        self.pos += 1
        return token
    
    def parse_expression(self):
        left = self.consume()
        if left.isdigit():
            left = int(left)
        op = self.consume()
        right = self.consume()
        if right.isdigit():
            right = int(right)
        return (op, left, right)

    def parse_if_else(self):
        self.consume()  # consume 'if'
        condition = self.parse_expression()
        self.consume()  # consume '{'
        if_body = self.consume()
        self.consume()  # consume '}'
        if self.peek() == 'else':
            self.consume()
            self.consume()  # consume '{'
            else_body = self.consume()
            self.consume()  # consume '}'
            return ('if-else', condition, if_body, else_body)
        return ('if', condition, if_body)
    
    def parse_for_loop(self):
        self.consume()  # consume 'for'
        
        # Parse initialization (e.g., i = 0)
        init = self.parse_expression()
        self.consume()  # consume ';'
        
        # Parse condition (e.g., i < 10)
        condition = self.parse_expression()
        self.consume()  # consume ';'
        
        # Parse update expression (e.g., i = i + 1)
        # For now, since we can't handle complex expressions properly,
        # let's hardcode the increment operation
        var_name = self.consume()  # should be 'i'
        self.consume()  # consume '='
        self.consume()  # consume 'i'
        self.consume()  # consume '+'
        increment = self.consume()  # consume '1'
        
        update = ('=', var_name, ('+', var_name, int(increment)))
        
        # Parse body
        self.consume()  # consume '{'
        body = self.consume()
        self.consume()  # consume '}'
        
        return ('for', init, condition, update, body)
    
    def parse_function(self):
        self.consume()  # consume 'function'
        func_name = self.consume()
        
        self.consume()  # consume '('
        
        # Parse parameters
        params = []
        while self.peek() != ')':
            params.append(self.consume())
            if self.peek() == ',':
                self.consume()  # consume ','
        
        self.consume()  # consume ')'
        self.consume()  # consume '{'
        
        # Parse body (for simplicity, just one expression)
        body = self.consume()
        
        self.consume()  # consume '}'
        
        return ('function', func_name, params, body)
    
    def parse(self):
        if self.peek() == 'if':
            return self.parse_if_else()
        elif self.peek() == 'for':
            return self.parse_for_loop()
        return self.parse_expression()

class Environment:
    def __init__(self, parent=None):
        self.variables = {}
        self.functions = {}
        self.parent = parent
    
    def get(self, name):
        if name in self.variables:
            return self.variables[name]
        if self.parent:
            return self.parent.get(name)
        raise NameError(f"Variable '{name}' not defined")
    
    def set(self, name, value):
        self.variables[name] = value
        return value
    
    def define_function(self, name, params, body):
        self.functions[name] = (params, body)
    
    def get_function(self, name):
        if name in self.functions:
            return self.functions[name]
        if self.parent:
            return self.parent.get_function(name)
        raise NameError(f"Function '{name}' not defined")

def evaluate(ast, variables=variables):
    # Handle primitive types (int, str that are not variable names)
    if isinstance(ast, int):
        return ast
    elif isinstance(ast, str) and ast not in variables:
        try:
            return int(ast)  # Try to convert to int if it's a number string
        except ValueError:
            return ast  # Return as is if it's not a number
    
    # Continue with the existing code
    if ast[0] == '=':
        # Variable assignment: var = value
        _, var_name, value_expr = ast
        variables[var_name] = evaluate(value_expr, variables)
        return variables[var_name]
    elif isinstance(ast, str) and ast in variables:
        # Variable lookup
        return variables[ast]
    if ast[0] in ('+', '-', '*', '/', '>', '<', '==', '!=', '>=', '<='):
        op, left, right = ast
        # Evaluate the operands first
        left_val = evaluate(left, variables)
        right_val = evaluate(right, variables)
        
        # Now compare the evaluated values
        if op == '>':
            return left_val > right_val
        elif op == '<':
            return left_val < right_val
        elif op == '==':
            return left_val == right_val
        elif op == '!=':
            return left_val != right_val
        elif op == '>=':
            return left_val >= right_val
        elif op == '<=':
            return left_val <= right_val
        else:
            return eval(f"{left_val} {op} {right_val}")
    elif ast[0] == 'if-else':
        _, condition, if_body, else_body = ast
        if evaluate(condition, variables):
            # print("if_body:", if_body)
            return if_body
        else:
            return else_body
    elif ast[0] == 'if':
        _, condition, if_body = ast
        if evaluate(condition, variables):
            return if_body
    elif ast[0] == 'for':
        _, init, condition, update, body = ast
        
        # Execute initialization
        evaluate(init, variables)
        
        # Check condition, execute body, update, and repeat
        while evaluate(condition, variables):
            result = evaluate(body, variables)
            evaluate(update, variables)
            
        return result
    return None

# Example usage:
code = "for i = 0; i < 5; i = i + 1 { i }"
tokens = tokenize(code)
parser = Parser(tokens)
ast = parser.parse()
print("AST:", ast)
print("Execution Result:", evaluate(ast))  # Should print the final value of i (4)
