# parser.py

from lexer import *

# AST Node Definitions
class ASTNode:
    pass

class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements
    def __repr__(self):
        return f"Program({self.statements})"

class ExpressionStatement(ASTNode):
    def __init__(self, expression):
        self.expression = expression
    def __repr__(self):
        return f"ExprStmt({self.expression})"

class PrintStatement(ASTNode):
    def __init__(self, expression):
        self.expression = expression
    def __repr__(self):
        return f"Print({self.expression})"

class BlockStatement(ASTNode):
    def __init__(self, statements):
        self.statements = statements
    def __repr__(self):
        return f"Block({self.statements})"

class IfStatement(ASTNode):
    def __init__(self, condition, then_branch, else_branch):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch
    def __repr__(self):
        return f"If({self.condition}, {self.then_branch}, {self.else_branch})"

class WhileStatement(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
    def __repr__(self):
        return f"While({self.condition}, {self.body})"

class ForStatement(ASTNode):
    def __init__(self, initializer, condition, increment, body):
        self.initializer = initializer
        self.condition = condition
        self.increment = increment
        self.body = body
    def __repr__(self):
        return f"For({self.initializer}, {self.condition}, {self.increment}, {self.body})"

class Binary(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right
    def __repr__(self):
        return f"Binary({self.left}, {self.operator.value}, {self.right})"

class Unary(ASTNode):
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right
    def __repr__(self):
        return f"Unary({self.operator.value}, {self.right})"

class Grouping(ASTNode):
    def __init__(self, expression):
        self.expression = expression
    def __repr__(self):
        return f"Grouping({self.expression})"

class Literal(ASTNode):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"Literal({self.value})"

class Variable(ASTNode):
    def __init__(self, token):
        self.name = token.value
    def __repr__(self):
        return f"Variable({self.name})"

class Assignment(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value
    def __repr__(self):
        return f"Assign({self.name}, {self.value})"


# Parser Implementation
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        statements = []
        while not self.is_at_end():
            statements.append(self.declaration())
        return Program(statements)

    def declaration(self):
        # You can later add support for function/variable declarations.
        return self.statement()

    def statement(self):
        if self.match(TokenType.IF):
            return self.if_statement()
        if self.match(TokenType.WHILE):
            return self.while_statement()
        if self.match(TokenType.FOR):
            return self.for_statement()
        if self.match(TokenType.PRINT):
            return self.print_statement()
        if self.match(TokenType.LEFT_BRACE):
            return BlockStatement(self.block())
        return self.expression_statement()

    def if_statement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'agar'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after if condition.")
        then_branch = self.statement()
        else_branch = None
        if self.match(TokenType.ELSE):
            else_branch = self.statement()
        return IfStatement(condition, then_branch, else_branch)

    def while_statement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'jabtak'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after while condition.")
        body = self.statement()
        return WhileStatement(condition, body)

    def for_statement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'karo'.")
        initializer = self.expression_statement()
        condition = self.expression_statement()
        increment = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after for clauses.")
        body = self.statement()
        return ForStatement(initializer, condition, increment, body)

    def print_statement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'likho'.")
        expr = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after print expression.")
        self.consume(TokenType.SEMICOLON, "Expect ';' after print statement.")
        return PrintStatement(expr)

    def expression_statement(self):
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return ExpressionStatement(expr)

    def block(self):
        statements = []
        while not self.check(TokenType.RIGHT_BRACE) and not self.is_at_end():
            statements.append(self.declaration())
        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
        return statements

    def expression(self):
        return self.assignment()

    def assignment(self):
        expr = self.equality()
        if self.match(TokenType.ASSIGN):
            equals = self.previous()
            value = self.assignment()
            if isinstance(expr, Variable):
                return Assignment(expr.name, value)
            self.error(equals, "Invalid assignment target.")
        return expr

    def equality(self):
        expr = self.comparison()
        while self.match(TokenType.EQUALS, TokenType.NOT_EQUALS):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)
        return expr

    def comparison(self):
        expr = self.term()
        while self.match(TokenType.LESS_THAN, TokenType.GREATER_THAN):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)
        return expr

    def term(self):
        expr = self.factor()
        while self.match(TokenType.PLUS, TokenType.MINUS):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)
        return expr

    def factor(self):
        expr = self.unary()
        while self.match(TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)
        return expr

    def unary(self):
        if self.match(TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)
        return self.primary()

    def primary(self):
        if self.match(TokenType.INTEGER_LITERAL, TokenType.FLOAT_LITERAL,
                      TokenType.STRING_LITERAL, TokenType.CHAR_LITERAL):
            return Literal(self.previous().value)
        if self.match(TokenType.IDENTIFIER):
            return Variable(self.previous())
        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)
        self.error(self.peek(), "Expect expression.")

    # Utility methods
    def match(self, *token_types):
        for t in token_types:
            if self.check(t):
                self.advance()
                return True
        return False

    def consume(self, token_type, message):
        if self.check(token_type):
            return self.advance()
        self.error(self.peek(), message)

    def check(self, token_type):
        if self.is_at_end():
            return False
        return self.peek().type == token_type

    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self):
        return self.peek().type == TokenType.EOF

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]

    def error(self, token, message):
        raise Exception(f"[line {token.line}] Error at '{token.value}': {message}")


# Example of usage with your lexer
if __name__ == "__main__":
    # Suppose `source_code` is your input file string.
    source_code = """
    agar (x < 10) {
        likho("x is less than 10");
    } nahi_to {
        likho("x is 10 or greater");
    }
    """
    # Assuming you have already imported your Lexer and TokenType classes from lexer.py:
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()
    print("tokens by lexer:", tokens)
    parser = Parser(tokens)
    ast = parser.parse()
    print("ast generated successfully!")
    print(ast)
