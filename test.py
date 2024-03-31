from parser.grammar import G, equal, plus, num, sym_set
from parser.parser import LR1Parser
from common.pycompiler import NonTerminal, Terminal
from lexer.lexer import Lexer
my_parser = LR1Parser(G, True)

my_lexer = Lexer('1 + 2 = 3').tokens
#print(sym_set[my_lexer[0].token_type])
parse = list(map(lambda x: sym_set[x.token_type], my_lexer))
print(my_parser(parse))
