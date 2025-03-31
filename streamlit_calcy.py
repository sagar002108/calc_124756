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

# Parser (Syntax Analysis) supporting Prefix and Infix Notation
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

    # Infix notation (4 + 6)
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

    # Prefix notation support (+ 4 6 → 4 + 6)
    @_('PLUS expr expr')
    def expr(self, p):
        return p.expr0 + p.expr1

    @_('MINUS expr expr')
    def expr(self, p):
        return p.expr0 - p.expr1

    @_('TIMES expr expr')
    def expr(self, p):
        return p.expr0 * p.expr1

    @_('DIVIDE expr expr')
    def expr(self, p):
        return p.expr0 / p.expr1 if p.expr1 != 0 else "Error: Division by zero"

    # Handling single operators at start of input (+ 4 6)
    @_('PLUS NUMBER NUMBER')
    def expr(self, p):
        return p.NUMBER0 + p.NUMBER1

    @_('MINUS NUMBER NUMBER')
    def expr(self, p):
        return p.NUMBER0 - p.NUMBER1

    @_('TIMES NUMBER NUMBER')
    def expr(self, p):
        return p.NUMBER0 * p.NUMBER1

    @_('DIVIDE NUMBER NUMBER')
    def expr(self, p):
        return p.NUMBER0 / p.NUMBER1 if p.NUMBER1 != 0 else "Error: Division by zero"

# Streamlit UI
st.set_page_config(page_title="PPI Calculator", page_icon="🧮", layout="centered")

st.markdown("<h1 style='text-align: center;'>🧮 PPI Calculator</h1>", unsafe_allow_html=True)

expression = st.text_input("Enter Expression:", placeholder="e.g., 3 + 5 * (2 - 1) or + 4 6")

if st.button("Calculate 🧮"):
    lexer = CalcLexer()
    parser = CalcParser()
    
    try:
        tokens = iter(lexer.tokenize(expression))
        result = parser.parse(tokens)
        if result is not None:
            st.success(f"✅ Result: {result}")
        else:
            st.error("❌ Invalid expression!")
    except Exception as e:
        st.error(f"❌ Error: {e}")
