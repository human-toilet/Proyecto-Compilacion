from parser.lr1_automaton import build_LR1_automaton

class ShiftReduceParser:
    SHIFT = 'SHIFT'
    REDUCE = 'REDUCE'
    OK = 'OK'
    
    def __init__(self, G, verbose=False):
        self.G = G
        self.verbose = verbose
        self.action = {}
        self.goto = {}
        self._build_parsing_table()
    
    def _build_parsing_table(self):
        raise NotImplementedError()

    def __call__(self, w):
        stack = [ 0 ]
        cursor = 0
        output = []
        
        while True:
            state = stack[-1]
            lookahead = w[cursor]
            if self.verbose: print(stack, '<---||--->', w[cursor:])
            try:
                action, tag = self.action[state, lookahead]            
            except:
                raise Exception("Syntax Error")
            match action:
                case self.SHIFT:
                    stack.append(lookahead)
                    stack.append(tag)
                    cursor += 1
                case self.REDUCE:
                    production = self.G.Productions[tag]
                    X, beta = production
                    for i in range(2 * len(beta)):
                        stack.pop()
                    l = stack[-1]
                    stack.append(X.Name)
                    stack.append(self.goto[l,X])
                    output.append(production)
                case self.OK:
                    break
                case _:
                    raise Exception
        
        return output
    

class LR1Parser(ShiftReduceParser):
    def _build_parsing_table(self):
        G = self.G.AugmentedGrammar(True)
        
        automaton = build_LR1_automaton(G)
        for i, node in enumerate(automaton):
            if self.verbose: print(i, '\t', '\n\t '.join(str(x) for x in node.state), '\n')
            node.idx = i

        for node in automaton:
            idx = node.idx
            for item in node.state:
        
                X = item.production.Left
                symbol = item.NextSymbol
                if X == G.startSymbol and item.IsReduceItem:
                    self._register(self.action,(idx,G.EOF),(self.OK,0))
                elif item.IsReduceItem:
                    k = self.G.Productions.index(item.production)
                    for s in item.lookaheads:                        
                        self._register(self.action,(idx,s),(self.REDUCE,k))
                elif symbol.IsTerminal:
                    self._register(self.action,(idx,symbol),(self.SHIFT,node.transitions[symbol.Name][0].idx))
                else:
                    self._register(self.goto,(idx,symbol),node.transitions[symbol.Name][0].idx)
        
    @staticmethod
    def _register(table, key, value):
        assert key not in table or table[key] == value, 'Shift-Reduce or Reduce-Reduce conflict!!!'
        table[key] = value