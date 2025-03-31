import streamlit as st
from sly import Lexer, Parser

# Lexer (Lexical Analysis)
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

# Parser (Syntax Analysis)
class CalcParser(Parser):
    tokens = CalcLexer.tokens
    precedence = (('left', PLUS, MINUS), ('left', TIMES, DIVIDE), ('right', 'UMINUS'))

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

# Streamlit UI Setup
st.title("🧮  Professional Multi-Mode Calculator")

# Session state to store input
if "input_text" not in st.session_state:
    st.session_state.input_text = ""
if "history" not in st.session_state:
    st.session_state.history = []

# Layout: Calculator Buttons
buttons = [
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["0", "(", ")", "+"]
]

col1, col2 = st.columns([2, 1])

with col1:
    st.text_input("Expression:", value=st.session_state.input_text, key="display", disabled=True)

    # Button grid
    for row in buttons:
        cols = st.columns(4)
        for i, label in enumerate(row):
            if cols[i].button(label):
                st.session_state.input_text += label

    # Extra functions
    cols = st.columns(4)
    if cols[0].button("C"):
        st.session_state.input_text = ""
    if cols[1].button("←"):
        st.session_state.input_text = st.session_state.input_text[:-1]
    if cols[2].button("="):
        try:
            lexer = CalcLexer()
            tokens = iter(lexer.tokenize(st.session_state.input_text))
            parser = CalcParser()
            result = parser.parse(tokens)
            st.session_state.history.append(f"{st.session_state.input_text} = {result}")
            st.session_state.input_text = str(result)
        except Exception:
            st.session_state.input_text = "Error"

with col2:
    st.write("### History")
    for entry in st.session_state.history[-5:]:  
        st.write(entry)
