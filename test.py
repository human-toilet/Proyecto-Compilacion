from parser.grammar import gramm_Hulk_LR1
from parser.parser import LR1Parser
from common.pycompiler import NonTerminal, Terminal
from lexer.lexer import Lexer
from parser.evaluate import evaluate_reverse_parse
gramar, sym_set = gramm_Hulk_LR1()
my_parser = LR1Parser(gramar, True)

text = "let a = 1 in {print(a);};"

with open('./prueba.txt', "r") as archivo:
    # Lee todas las líneas del archivo
    lineas = archivo.readlines()
    # Une todas las líneas en una sola cadena
    contenido = "".join(lineas)
    contenido = contenido.replace('\n', ' ')

    # Reemplazar tabulaciones por espacios en blanco
    contenido = contenido.replace('\t', '')
    contenido = contenido.replace('"', '\"')
#    text = contenido

my_lexer = Lexer(text).tokens
print(my_lexer)
parse = list(map(lambda x: sym_set[x.token_type], my_lexer))
right_parse, operatons = my_parser(parse)
print(evaluate_reverse_parse(right_parse, operatons, parse))


    
#print(sym_set[my_lexer[0].token_type])


