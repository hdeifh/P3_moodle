import ply.yacc as yacc
from src.roman_lexer import tokens

# Gramática

def p_romanNumber(p):
    pass


def p_thousand(p):
    pass


def p_small_hundred(p):
    pass


def p_hundred(p):
    pass


def p_small_ten(p):
    pass

def p_ten(p):
    pass


def p_small_digit(p):
    pass

def p_digit(p):
    pass

# Definir lambda
def p_empty(p):
    'lambda :'
    pass

def p_roman(p):
    pass

# Manejo de errores sintácticos
def p_error(p):
    print("Error de sintaxis en '%s'" % p.value if p else "EOF")

# Construir el parser
parser = yacc.yacc()

if __name__ == "__main__":
    while True:
        try:
            s = input("Ingrese un número romano: ")
        except EOFError:
            break
        if not s:
            continue
        result = parser.parse(s)
        print(f"El valor numérico es: {result}")

