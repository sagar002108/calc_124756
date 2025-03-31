import streamlit as st
from sly import Lexer, Parser

# Lexer (Lexical Analysis)
class CalcLexer(Lexer):
    tokens = {NUMBER, PLUS, MINUS, TIMES, DIVIDE, LPAREN, RPAREN}
    ignore = ' \t'

    NUMBER = r'-?\d+'  # Allow negative numbers
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    LPAREN = r'\('
    RPAREN = r'\)'

    def NUMBER(self, t):
        t.value = int(t.value)  # Convert NUMBER token to integer
        return t

# Parser (Syntax Analysis)
class CalcParser(Parser):
    tokens = CalcLexer.tokens

    precedence = (
        ('left', PLUS, MINUS),
        ('left', TIMES, DIVIDE),
        ('right', 'UMINUS')  # Handle negative numbers
    )

    @_('expr')
    def statement(self, p):
        return p.expr  # Ensure valid expressions return a value

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

# Streamlit UI
st.title("🧮  Multi-Mode Calculator")

# Input field for the expression
expression = st.text_input("Enter Expression (e.g., 7 - 3):")

if st.button("Calculate"):
    try:
        lexer = CalcLexer()
        tokens = list(lexer.tokenize(expression))  # Ensure tokens are iterable
        parser = CalcParser()
        result = parser.parse(iter(tokens))  # Ensure parsing works
        st.success(f"Result: {result}")
    except Exception as e:
        st.error(f"Error: {e}")
