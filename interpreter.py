from SQLLexer import SQLLexer
from SQLParser import SQLParser

class SQLInterpreter:
    """Main interpreter class that handles the REPL"""
    
    def __init__(self):
        self.lexer = SQLLexer()
        self.parser = SQLParser(self.lexer)
        self.buffer = ""

    def run(self):
        print("Interprete SQL para CSV. Escribe 'quit;' para salir.")
        
        while True:
            try:
                line = input("SQL > ")
                if line.strip().lower() in ('quit;', 'exit;'):
                    print("Bye.")
                    break

                self.buffer += line
                if ';' in self.buffer:
                    print(f"DEBUG: Comando completo recibido: {self.buffer}")
                    self.parser.parser.parse(self.buffer)
                    self.buffer = ""
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    interpreter = SQLInterpreter()
    interpreter.run()