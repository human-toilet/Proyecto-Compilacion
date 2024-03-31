from parser.grammar import G, equal, plus, num
from parser.parser import LR1Parser
from common.pycompiler import NonTerminal, Terminal
my_parser = LR1Parser(G, True)

print(my_parser([num, equal, num, plus, num, G.EOF]))
