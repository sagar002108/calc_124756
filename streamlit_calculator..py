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

# Streamlit UI
st.title("🧮 Streamlit Calculator")
expression = st.text_input("Enter expression:")

if st.button("Calculate"):
    lexer = CalcLexer()
    parser = CalcParser()
    try:
        tokens = iter(lexer.tokenize(expression))  # Convert list to iterator
        result = parser.parse(tokens)
        st.success(f"Result: {result}")
    except Exception as e:
        st.error(f"Error: {e}")


