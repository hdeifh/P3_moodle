import ply.yacc as yacc
from src.g1_lexer import tokens

# Gramática


def p_Language(p):
    pass

def p_A(p):
    """A : a A
        | lambda"""

    pass
def p_B(p):
    """B : b B
        | lambda"""
    pass

def p_C(p):
    """C : c C
        | lambda"""
    if len(p) == 3:
        p[0] = {"c": 1 + p[2]["c"]}
    else:
        p[0] = {"c": 0}

def p_lambda(p):
    """lambda :"""
    pass  # Producción vacía

# Manejo de errores sintácticos
def p_error(p):
    print("Error de sintaxis en '%s'" % p.value if p else "EOF")

# Construir el parser
parser = yacc.yacc()

if __name__ == "__main__":
    while True:
        try:
            s = input("Ingrese una cadena: ")
        except EOFError:
            break
        if not s:
            continue
        result = parser.parse(s)
        print(f"El valor numérico es:", result)

