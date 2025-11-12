import ply.lex as lex

# Lista de tokens que necesitamos para los números romanos
tokens = (
    'M', 'D', 'C', 'L', 'X', 'V', 'I'
)

# Expresiones regulares para los tokens
t_M = r'M'
t_D = r'D'
t_C = r'C'
t_L = r'L'
t_X = r'X'
t_V = r'V'
t_I = r'I'

# Ignorar espacios en blanco
t_ignore = ' \t\n'

# Manejo de errores de caracteres no reconocidos
def t_error(t):
    print(f"Caracter ilegal: {t.value[0]}")
    raise Exception("Caracter ilegal")

# Construir el lexer
lexer = lex.lex()

if __name__ == "__main__":
    # Prueba del lexer
    data = 'MCMXCIV'
    lexer.input(data)

    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)

