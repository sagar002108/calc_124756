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
        t.value = int(t.value)
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
        return p.expr

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
st.set_page_config(page_title="Calculator", page_icon="🧮", layout="centered")

st.markdown(
    """
    <style>
        .calculator {
            display: grid;
            grid-template-columns: repeat(4, 80px);
            gap: 10px;
            justify-content: center;
        }
        .button {
            width: 80px;
            height: 80px;
            font-size: 24px;
            font-weight: bold;
            text-align: center;
            border-radius: 10px;
            border: none;
            background-color: #f1f1f1;
            cursor: pointer;
            transition: 0.3s;
        }
        .button:hover {
            background-color: #ddd;
        }
        .display {
            width: 340px;
            height: 80px;
            text-align: right;
            font-size: 32px;
            font-weight: bold;
            padding: 10px;
            border-radius: 10px;
            border: 2px solid #ccc;
            background-color: #fff;
            margin-bottom: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 style='text-align: center;'>🧮 Calculator</h1>", unsafe_allow_html=True)

# Store the calculator input
if "expression" not in st.session_state:
    st.session_state.expression = ""

# Display Screen
st.markdown(f"<div class='display'>{st.session_state.expression}</div>", unsafe_allow_html=True)

# Buttons for the calculator
buttons = [
    "7", "8", "9", "/",
    "4", "5", "6", "*",
    "1", "2", "3", "-",
    "0", "C", "=", "+"
]

# Define button click event
def button_click(btn):
    if btn == "C":
        st.session_state.expression = ""  # Clear input
    elif btn == "=":
        try:
            lexer = CalcLexer()
            tokens = list(lexer.tokenize(st.session_state.expression))
            parser = CalcParser()
            result = parser.parse(iter(tokens))
            st.session_state.expression = str(result)
        except Exception:
            st.session_state.expression = "Error"
    else:
        st.session_state.expression += btn  # Append button value

# Display Buttons in Grid
cols = st.columns(4)
for index, btn in enumerate(buttons):
    with cols[index % 4]:
        st.button(btn, key=btn, on_click=button_click, args=(btn,))
