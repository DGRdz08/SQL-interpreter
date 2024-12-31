import ply.yacc as yacc
from handler.data_handler import DataHandler

class SQLParser:
    """Parser for SQL-like commands"""
    
    def __init__(self, lexer):
        self.lexer = lexer
        self.tokens = lexer.tokens
        self.parser = yacc.yacc(module=self)
        self.data_handler = DataHandler()

    def p_statement_select(self, p):
        """statement : SELECT columns FROM table WHERE conditions eos
                     | SELECT columns FROM table eos
                     | SELECT ASTERISK FROM table WHERE conditions eos
                     | SELECT ASTERISK FROM table eos"""
        filename = p[4]
        columns = p[2]
        conditions = p[len(p)-2] if len(p) in [7, 8] and p[len(p)-2] != 'eos' else None
        self.data_handler.execute_select(filename, columns, conditions)

    def p_statement_insert(self, p):
        """statement : INSERT INTO table VALUES LPAREN values RPAREN eos"""
        filename = p[3]
        values = p[6]
        self.data_handler.execute_insert(filename, values)

    def p_statement_update(self, p):
        """statement : UPDATE table SET set_clauses WHERE conditions eos
                      | UPDATE table SET set_clauses eos"""
        filename = p[2]
        set_clauses = p[4]
        conditions = p[6] if len(p) == 8 else None
        print(f"DEBUG: Condiciones pasadas al manejador: {conditions}")
        self.data_handler.execute_update(filename, set_clauses, conditions)

    def p_statement_delete(self, p):
        """statement : DELETE FROM table WHERE conditions eos
                      | DELETE FROM table eos"""
        filename = p[3]
        conditions = p[5] if len(p) == 7 else None
        self.data_handler.execute_delete(filename, conditions)

    def p_columns(self, p):
        """columns : columns COMMA column
                   | column"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_column(self, p):
        """column : IDENTIFIER"""
        p[0] = p[1]

    def p_table(self, p):
        """table : STRING"""
        p[0] = p[1]

    def p_values(self, p):
        """values : values COMMA value
                  | value"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_value(self, p):
        """value : NUMBER
                 | STRING"""
        p[0] = p[1]

    def p_set_clauses(self, p):
        """set_clauses : set_clauses COMMA set_clause
                       | set_clause"""
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = p[1] + ", " + p[3]

    def p_set_clause(self, p):
        """set_clause : column EQUALS value"""
        p[0] = f"{p[1]} = {p[3]}"

    def p_conditions(self, p):
        """conditions : conditions logical condition
                      | condition"""
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = f"{p[1]} {p[2]} {p[3]}"

    def p_condition(self, p):
        """condition : column EQUALS value
                      | column GREATER value
                      | column LESS value"""
        p[0] = f"{p[1]} {p[2]} {p[3]}"

    def p_logical(self, p):
        """logical : AND
                   | OR"""
        p[0] = p[1]

    def p_eos(self, p):
        """eos : SEMICOLON"""
        pass

    def p_error(self, p):
        if p:
            print(f"Syntax error at '{p.value}'")
        else:
            print("Syntax error at EOF")
