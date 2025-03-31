import streamlit as st
from sly import Lexer, Parser

# Lexer (Lexical Analysis)
class CalcLexer(Lexer):
    tokens = {NUMBER, PLUS, MINUS, TIMES, DIVIDE, LPAREN, RPAREN}
    ignore = ' \t'

    # Token definitions
    NUMBER = r'-?\d+'  # Allows negative numbers
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

# Streamlit UI Design
st.set_page_config(page_title="Calculator", page_icon="🧮", layout="centered")

st.markdown(
    """
    <style>
    body {
        background-color: #F4F4F4;
        color: #333333;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .stApp {
        background-color: #FFFFFF;
        padding: 30px;
        border-radius: 12px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
    }
    .stTextInput>div>div>input {
        font-size: 20px;
        text-align: center;
        background-color: #E8E8E8;
        color: #333333;
        border: 2px solid #C1C1C1;
        border-radius: 6px;
        padding: 10px;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-size: 18px;
        border-radius: 6px;
        padding: 12px 25px;
        border: none;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #45A049;
    }
    .stAlert {
        font-size: 18px;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🧮 Simple Calculator")
st.markdown("Enter your mathematical expression below and press Calculate.")

expression = st.text_input("Expression", placeholder="e.g., -3 + 5 * (2 - 1)")

if st.button("Calculate"):
    lexer = CalcLexer()
    parser = CalcParser()
    try:
        tokens = iter(lexer.tokenize(expression))  # Convert list to iterator
        result = parser.parse(tokens)
        st.success(f"Result: {result}")
    except Exception as e:
        st.error(f"Error: {e}")
