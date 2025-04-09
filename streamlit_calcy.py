import streamlit as st
from sly import Lexer, Parser

# Lexer
class CalcLexer(Lexer):
    tokens = {
        NUMBER, PLUS, MINUS, TIMES, DIVIDE,
        LPAREN, RPAREN,
        PLUS_WORD, MINUS_WORD, TIMES_WORD, DIVIDE_WORD
    }
    ignore = ' \t'

    # Token patterns
    NUMBER = r'-?\d+'
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    LPAREN = r'\('
    RPAREN = r'\)'

    PLUS_WORD = r'plus'
    MINUS_WORD = r'minus'
    TIMES_WORD = r'times'
    DIVIDE_WORD = r'divide'

    def NUMBER(self, t):
        t.value = int(t.value)
        return t

# Parser for evaluation
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

    @_('expr PLUS expr')
    def expr(self, p): return p.expr0 + p.expr1

    @_('expr MINUS expr')
    def expr(self, p): return p.expr0 - p.expr1

    @_('expr TIMES expr')
    def expr(self, p): return p.expr0 * p.expr1

    @_('expr DIVIDE expr')
    def expr(self, p):
        if p.expr1 == 0:
            raise ZeroDivisionError("Division by zero")
        return p.expr0 / p.expr1

    @_('MINUS expr %prec UMINUS')
    def expr(self, p): return -p.expr

    @_('LPAREN expr RPAREN')
    def expr(self, p): return p.expr

    @_('NUMBER')
    def expr(self, p): return p.NUMBER

    # Prefix word-based operations
    @_('PLUS_WORD expr expr')
    def expr(self, p): return p.expr0 + p.expr1

    @_('MINUS_WORD expr expr')
    def expr(self, p): return p.expr0 - p.expr1

    @_('TIMES_WORD expr expr')
    def expr(self, p): return p.expr0 * p.expr1

    @_('DIVIDE_WORD expr expr')
    def expr(self, p):
        if p.expr1 == 0:
            raise ZeroDivisionError("Division by zero")
        return p.expr0 / p.expr1

    # Symbol-based prefix
    @_('PLUS expr expr')
    def expr(self, p): return p.expr0 + p.expr1

    @_('MINUS expr expr')
    def expr(self, p): return p.expr0 - p.expr1

    @_('TIMES expr expr')
    def expr(self, p): return p.expr0 * p.expr1

    @_('DIVIDE expr expr')
    def expr(self, p):
        if p.expr1 == 0:
            raise ZeroDivisionError("Division by zero")
        return p.expr0 / p.expr1

# Parser for infix expression generation
class InfixConverter(Parser):
    tokens = CalcLexer.tokens

    @_('expr')
    def statement(self, p):
        return p.expr

    @_('')
    def statement(self, p):
        return ""

    @_('expr PLUS expr')
    def expr(self, p): return f"({p.expr0} + {p.expr1})"

    @_('expr MINUS expr')
    def expr(self, p): return f"({p.expr0} - {p.expr1})"

    @_('expr TIMES expr')
    def expr(self, p): return f"({p.expr0} * {p.expr1})"

    @_('expr DIVIDE expr')
    def expr(self, p): return f"({p.expr0} / {p.expr1})"

    @_('MINUS expr %prec UMINUS')
    def expr(self, p): return f"-{p.expr}"

    @_('LPAREN expr RPAREN')
    def expr(self, p): return p.expr

    @_('NUMBER')
    def expr(self, p): return str(p.NUMBER)

    # Prefix (words and symbols)
    @_('PLUS_WORD expr expr', 'PLUS expr expr')
    def expr(self, p): return f"({p.expr0} + {p.expr1})"

    @_('MINUS_WORD expr expr', 'MINUS expr expr')
    def expr(self, p): return f"({p.expr0} - {p.expr1})"

    @_('TIMES_WORD expr expr', 'TIMES expr expr')
    def expr(self, p): return f"({p.expr0} * {p.expr1})"

    @_('DIVIDE_WORD expr expr', 'DIVIDE expr expr')
    def expr(self, p): return f"({p.expr0} / {p.expr1})"

# Streamlit UI
st.set_page_config(page_title="PPI Calculator", page_icon="🧮", layout="centered")
st.markdown("<h1 style='text-align: center;'>🧮 PPI Calculator</h1>", unsafe_allow_html=True)
st.markdown("Supports standard & prefix notation (e.g., `+ 1 2`, `* 1 + 2 3`)")

expression = st.text_input("Enter Expression:", placeholder="e.g., 3 + 5 * (2 - 1) or + 1 2")

if st.button("Calculate 🧮"):
    if expression.strip() == "":
        st.warning("⚠️ Please enter a valid expression.")
    else:
        lexer = CalcLexer()
        parser = CalcParser()
        infix = InfixConverter()

        try:
            tokens_for_eval = iter(lexer.tokenize(expression))
            tokens_for_infix = iter(lexer.tokenize(expression))

            result = parser.parse(tokens_for_eval)
            infix_expr = infix.parse(tokens_for_infix)

            st.success(f"✅ Result: {result}")
            st.info(f"📝 Infix Notation: `{infix_expr}`")
        except ZeroDivisionError as zde:
            st.error(f"❌ Error: {zde}")
        except Exception as e:
            st.error(f"❌ Error: {e}")
