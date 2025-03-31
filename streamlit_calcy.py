import streamlit as st
from sly import Lexer, Parser

# Lexer (Lexical Analysis)
class CalcLexer(Lexer):
    tokens = {NUMBER, PLUS, MINUS, TIMES, DIVIDE, LPAREN, RPAREN}
    ignore = ' \t'

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
st.set_page_config(page_title="PPI Calculator", page_icon="🧮", layout="centered")

st.markdown(
    """
    <style>
        body {
            background-color: #0f172a;
            color: white;
            font-family: 'Arial', sans-serif;
        }
        .main-title {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            background: linear-gradient(90deg, #ff7e5f, #feb47b);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .stTextInput>div>div>input {
            border-radius: 10px;
            padding: 12px;
            font-size: 18px;
            text-align: center;
            border: 2px solid #ff7e5f;
            background-color: #1e293b;
            color: white;
        }
        .stButton>button {
            background: linear-gradient(90deg, #ff7e5f, #feb47b);
            color: white;
            font-size: 20px;
            border-radius: 12px;
            padding: 12px 24px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
            transition: 0.3s;
        }
        .stButton>button:hover {
            background: linear-gradient(90deg, #feb47b, #ff7e5f);
            transform: scale(1.05);
        }
        .result-box {
            text-align: center;
            font-size: 22px;
            font-weight: bold;
            color: #34eb8c;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 class='main-title'>🧮 PPI Calculator</h1>", unsafe_allow_html=True)

expression = st.text_input("Enter Expression:", placeholder="Type your math expression here...")

if st.button("Calculate 🧮"):
    lexer = CalcLexer()
    parser = CalcParser()
    
    try:
        tokens = iter(lexer.tokenize(expression))
        result = parser.parse(tokens)
        st.markdown(f"<div class='result-box'>✅ Result: {result}</div>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"❌ Error: {e}")
