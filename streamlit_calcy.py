# %%
import streamlit as st
from sly import Lexer, Parser

# Lexer (Lexical Analysis)
class CalcLexer(Lexer):
    tokens = {NUMBER, PLUS, MINUS, TIMES, DIVIDE, LPAREN, RPAREN}
    ignore = ' \t'

    # Token definitions
    NUMBER = r'\d+'
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
    )
    
    @_('expr')
    def statement(self, p):
        return p.expr
    
    @_('')
    def statement(self, p):
        return None  # Handles empty input
    
    # Handling infix notation and precedence
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
            if token.isdigit():
                stack.append(int(token))
            elif token in ('+', '-', '*', '/'):
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
            if token.isdigit():
                stack.append(int(token))
            elif token in ('+', '-', '*', '/'):
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

# Streamlit UI
st.title("🧮 Streamlit Calculator")
expression = st.text_input("Enter expression:")

if st.button("Calculate"):
    lexer = CalcLexer()
    parser = CalcParser()

    try:
        # Check if expression is in postfix notation (contains no operators like '+', '-', etc. between numbers)
        if ' ' in expression:
            if expression.strip().startswith(('+', '-', '*', '/')):  # Check if it starts with operator (prefix)
                result = parser.parse_prefix(expression)  # Process prefix expression
                st.success(f"Prefix Result: {result}")
            else:
                result = parser.parse_postfix(expression)  # Process postfix expression
                st.success(f"Postfix Result: {result}")
        else:
            tokens = iter(lexer.tokenize(expression))  # Convert list to iterator for infix evaluation
            result = parser.parse(tokens)  # Process infix expression
            st.success(f"Infix Result: {result}")
    except Exception as e:
        st.error(f"Error: {e}")



