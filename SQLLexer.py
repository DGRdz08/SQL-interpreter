import ply.lex as lex

class SQLLexer:
    """Lexical analyzer for SQL-like syntax"""
    
    tokens = (
        'IDENTIFIER', 'NUMBER', 'STRING', 'EQUALS', 'COMMA', 'SEMICOLON',
        'LPAREN', 'RPAREN', 'GREATER', 'LESS', 'ASTERISK'
    )

    reserved = {
        'select': 'SELECT',
        'from': 'FROM',
        'where': 'WHERE',
        'insert': 'INSERT',
        'into': 'INTO',
        'values': 'VALUES',
        'update': 'UPDATE',
        'set': 'SET',
        'delete': 'DELETE',
        'and': 'AND',
        'or': 'OR',
    }

    tokens = list(tokens) + list(reserved.values())

    # Regular expression rules for simple tokens
    t_SEMICOLON = r';'
    t_EQUALS = r'='
    t_COMMA = r','
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_GREATER = r'>'
    t_LESS = r'<'
    t_ASTERISK = r'\*'
    t_ignore = ' \t\n'

    def __init__(self):
        self.lexer = lex.lex(module=self)

    def t_IDENTIFIER(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value.lower(), 'IDENTIFIER')
        return t

    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_STRING(self, t):
        r'[\'"]([^\'"]*)[\'"]'
        t.value = t.value[1:-1]
        return t

    def t_error(self, t):
        print(f"Illegal character '{t.value[0]}'")
        t.lexer.skip(1)
