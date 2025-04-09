import streamlit as st
from sly import Lexer, Parser

# Lexer
class CalcLexer(Lexer):
    tokens = {NUMBER, PLUS, MINUS, TIMES, DIVIDE, LPAREN, RPAREN}
    ignore = ' \t'

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

# Parser
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
        return None

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

    # Postfix evaluation
    def parse_postfix(self, expr):
        stack = []
        tokens = expr.split()

        for token in tokens:
            if token.lstrip('-').isdigit():
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

    # Prefix evaluation
    def parse_prefix(self, expr):
        stack = []
        tokens = expr.split()[::-1]

        for token in tokens:
            if token.lstrip('-').isdigit():
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

    # Simple calculator
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

    # Prefix to readable infix
    def prefix_to_infix(self, expr):
        tokens = expr.split()[::-1]
        stack = []

        for token in tokens:
            if token.lstrip('-').isdigit():
                stack.append(token)
            elif token in ('+', '-', '*', '/'):
                if len(stack) < 2:
                    return "Error: Invalid Expression"
                a = stack.pop()
                b = stack.pop()
                stack.append(f"({a} {token} {b})")
        return stack[0] if stack else "Error: Invalid Expression"

    # Postfix to readable infix
    def postfix_to_infix(self, expr):
        tokens = expr.split()
        stack = []

        for token in tokens:
            if token.lstrip('-').isdigit():
                stack.append(token)
            elif token in ('+', '-', '*', '/'):
                if len(stack) < 2:
                    return "Error: Invalid Expression"
                b = stack.pop()
                a = stack.pop()
                stack.append(f"({a} {token} {b})")
        return stack[0] if stack else "Error: Invalid Expression"


# Streamlit UI
st.set_page_config(page_title="Calculator", layout="centered")
st.title("🧮 Multi-Mode Calculator")

calc_mode = st.selectbox("Select Calculation Mode", ["Simple Calculator", "Infix Notation", "Prefix Notation", "Postfix Notation"])
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

            elif calc_mode == "Prefix Notation":
                result = parser.parse_prefix(expression)
                readable = parser.prefix_to_infix(expression)
                st.success(f"Prefix Result: {result}")
                st.info(f"Readable Infix: {readable}")

            elif calc_mode == "Postfix Notation":
                result = parser.parse_postfix(expression)
                readable = parser.postfix_to_infix(expression)
                st.success(f"Postfix Result: {result}")
                st.info(f"Readable Infix: {readable}")

        except Exception as e:
            st.error(f"Error: {e}")
