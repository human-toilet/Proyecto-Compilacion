from parser.grammar import gramm_Hulk_LR1
from parser.parser import LR1Parser
from common.pycompiler import NonTerminal, Terminal
from lexer.lexer import Lexer
gramar = gramm_Hulk_LR1()
my_parser = LR1Parser(gramar[0], True)
 
my_lexer = Lexer('let a = 2 in { print(a + 3);}').tokens
print(my_lexer)
parse = list(map(lambda x: gramar[1][x.token_type], my_lexer))
print(my_parser(parse))

    
#print(sym_set[my_lexer[0].token_type])


