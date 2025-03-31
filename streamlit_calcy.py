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
            background-image: url("https://source.unsplash.com/1600x900/?calculator,technology");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            color: white;
            font-family: 'Roboto', sans-serif;
        }
        .overlay {
            background: rgba(0, 0, 0, 0.4);
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
        }
        .main-title {
            text-align: center;
            font-size: 48px;
            font-weight: bold;
            background: linear-gradient(90deg, #4f92d1, #2b6b8c);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.5);
            margin-top: 50px;
        }
        .stTextInput>div>div>input {
            border-radius: 12px;
            padding: 14px;
            font-size: 22px;
            text-align: center;
            border: 2px solid #4f92d1;
            background-color: rgba(255, 255, 255, 0.8);
            color: black;
        }
        .stButton>button {
            background: linear-gradient(90deg, #4f92d1, #2b6b8c);
            color: white;
            font-size: 24px;
            border-radius: 14px;
            padding: 16px 32px;
            box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.3);
            transition: 0.3s;
        }
        .stButton>button:hover {
            background: linear-gradient(90deg, #2b6b8c, #4f92d1);
            transform: scale(1.05);
        }
        .result-box {
            text-align: center;
            font-size: 26px;
            font-weight: bold;
            color: #34eb8c;
            padding: 12px;
            background-color: rgba(0, 0, 0, 0.7);
            border-radius: 12px;
            margin-top: 30px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<div class='overlay'></div>", unsafe_allow_html=True)
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
