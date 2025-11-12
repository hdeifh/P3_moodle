import ply.lex as lex

# Lista de tokens que necesitamos para los números romanos
tokens = (
    'a', 'b', 'c'
)

# Expresiones regulares para los tokens
t_a = r'a'
t_b = r'b'
t_c = r'c'

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
    data = 'a'
    lexer.input(data)

    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)

