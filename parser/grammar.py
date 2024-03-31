from common.pycompiler import Grammar

G = Grammar()
E = G.NonTerminal('E', True)
A = G.NonTerminal('A')
equal, plus, num = G.Terminals('= + int')

E %=  A + equal + A | num
A %= num + plus + A | num

sym_set = { 
    '<number>': num,
    '+': plus,
    '=': equal,
    'end': G.EOF
}