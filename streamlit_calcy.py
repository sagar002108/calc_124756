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
        t.value = int(t.value)  # Convert to integer
        return t

# Parser (Syntax Analysis)
class CalcParser(Parser):
    tokens = CalcLexer.tokens

    precedence = (
        ('left', PLUS, MINUS),
        ('left', TIMES, DIVIDE),
        ('right', 'UMINUS'),  # Handle unary minus
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
        return -p.expr  # Handle negative numbers

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
            background-image: url("https://png.pngtree.com/thumb_back/fh260/background/20200703/pngtree-mathematics-education-calculator-ruler-hand-drawn-background-image_340649.jpg");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            color: white;
            font-family: 'Arial', sans-serif;
        }
        .overlay {
            background: rgba(0, 0, 0, 0.6);
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
        }
        .main-title {
            text-align: center;
            font-size: 42px;
            font-weight: bold;
            background: linear-gradient(90deg, #ff7e5f, #feb47b);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
        .stTextInput>div>div>input {
            border-radius: 12px;
            padding: 14px;
            font-size: 20px;
            text-align: center;
            border: 2px solid #ff7e5f;
            background-color: rgba(255, 255, 255, 0.9);
            color: black;
        }
        .stButton>button {
            background: linear-gradient(90deg, #ff7e5f, #feb47b);
            color: white;
            font-size: 22px;
            border-radius: 14px;
            padding: 14px 28px;
            box-shadow: 0px 5px 12px rgba(0, 0, 0, 0.3);
            transition: 0.3s;
        }
        .stButton>button:hover {
            background: linear-gradient(90deg, #feb47b, #ff7e5f);
            transform: scale(1.08);
        }
        .result-box {
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            color: #34eb8c;
            padding: 10px;
            background-color: rgba(0, 0, 0, 0.6);
            border-radius: 12px;
            margin-top: 20px;
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
