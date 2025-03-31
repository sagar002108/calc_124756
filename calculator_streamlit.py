import streamlit as st
from sly import Lexer, Parser

# Lexer (Lexical Analysis)
class CalcLexer(Lexer):
    tokens = {NUMBER, PLUS, MINUS, TIMES, DIVIDE, LPAREN, RPAREN}
    ignore = ' \t'

    # Support negative numbers
    NUMBER = r'-?\d+'
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    LPAREN = r'\('
    RPAREN = r'\)'

    def NUMBER(self, t):
        t.value = int(t.value)
        return t

# Parser (Syntax Analysis)
class CalcParser(Parser):
    tokens = CalcLexer.tokens
    
    precedence = (
        ('left', PLUS, MINUS),
        ('left', TIMES, DIVIDE),
        ('right', 'UMINUS'),
    )

    @_('expr')
    def statement(self, p):
        return p.expr
    
    @_('')
    def statement(self, p):
        return None  # Handles empty input
    
    @_('expr PLUS expr')
    def expr(self, p):
        return p.expr0 + p.expr1
    
    @_('expr MINUS expr')
    def expr(self, p):
        return p.expr0 - p.expr1
    
    @_('expr TIMES expr')
    def expr(self, p):
        return p.expr0 * p.expr1
    
    @_('expr DIVIDE expr')
    def expr(self, p):
        return p.expr0 / p.expr1 if p.expr1 != 0 else "Error: Division by zero"
    
    @_('MINUS expr %prec UMINUS')
    def expr(self, p):
        return -p.expr

    @_('LPAREN expr RPAREN')
    def expr(self, p):
        return p.expr
    
    @_('NUMBER')
    def expr(self, p):
        return p.NUMBER

    # Postfix Expression Handling
    def parse_postfix(self, expr):
        stack = []
        tokens = expr.split()

        for token in tokens:
            if token.lstrip('-').isdigit():  # Handles negative numbers
                stack.append(int(token))
            elif token in ('+', '-', '*', '/'):
                if len(stack) < 2:
                    return "Error: Invalid Expression"
                b = stack.pop()
                a = stack.pop()
                if token == '+':
                    stack.append(a + b)
                elif token == '-':
                    stack.append(a - b)
                elif token == '*':
                    stack.append(a * b)
                elif token == '/':
                    stack.append(a / b if b != 0 else "Error: Division by zero")
        return stack[0] if stack else "Error: Invalid Expression"

    # Prefix Expression Handling
    def parse_prefix(self, expr):
        stack = []
        tokens = expr.split()[::-1]  # Reverse the tokens for prefix processing

        for token in tokens:
            if token.lstrip('-').isdigit():  # Handles negative numbers
                stack.append(int(token))
            elif token in ('+', '-', '*', '/'):
                if len(stack) < 2:
                    return "Error: Invalid Expression"
                a = stack.pop()
                b = stack.pop()
                if token == '+':
                    stack.append(a + b)
                elif token == '-':
                    stack.append(a - b)
                elif token == '*':
                    stack.append(a * b)
                elif token == '/':
                    stack.append(a / b if b != 0 else "Error: Division by zero")
        return stack[0] if stack else "Error: Invalid Expression"

    # Simple Calculator for Two Numbers
    def simple_calculator(self, num1, num2, operation):
        try:
            num1, num2 = float(num1), float(num2)
            if operation == '+':
                return num1 + num2
            elif operation == '-':
                return num1 - num2
            elif operation == '*':
                return num1 * num2
            elif operation == '/':
                return num1 / num2 if num2 != 0 else "Error: Division by zero"
        except ValueError:
            return "Error: Invalid Input"

# Streamlit UI
st.title("🧮  Multi-Mode Calculator")

# Dropdown to select mode
calc_mode = st.selectbox("Select Calculation Mode", ["Simple Calculator", "Infix Notation", "Prefix Notation", "Postfix Notation"])

# UI based on mode
parser = CalcParser()

if calc_mode == "Simple Calculator":
    num1 = st.text_input("Enter first number:")
    num2 = st.text_input("Enter second number:")
    operation = st.selectbox("Select operation", ["+", "-", "*", "/"])
    
    if st.button("Calculate"):
        result = parser.simple_calculator(num1, num2, operation)
        st.success(f"Result: {result}")

else:
    expression = st.text_input("Enter Expression:")

    if st.button("Calculate"):
        try:
            if calc_mode == "Infix Notation":
                lexer = CalcLexer()
                tokens = iter(lexer.tokenize(expression))
                result = parser.parse(tokens)
                st.success(f"Infix Result: {result}")

            elif calc_mode == "Postfix Notation":
                result = parser.parse_postfix(expression)
                st.success(f"Postfix Result: {result}")

            elif calc_mode == "Prefix Notation":
                result = parser.parse_prefix(expression)
                st.success(f"Prefix Result: {result}")

        except Exception as e:
            st.error(f"Error: {e}")
