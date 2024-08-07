from parser.lr1_automaton import build_LR1_automaton
from parser.SROperations import SROperations
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
        operations = []
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
                    stack.append(tag)
                    operations.append(self.SHIFT)
                    cursor += 1
                case self.REDUCE:
                    ##production = self.G.Productions[tag]
                    #X, beta = production
                    for _ in range(len(tag.Right)):
                        stack.pop()
                    stack.append(self.goto[stack[-1], tag.Left])
                    operations.append(self.REDUCE)
                    output.append(tag)
                case self.OK:
                    break
                case _:
                    raise Exception
        
        return output, operations
    

class LR1Parser(ShiftReduceParser):

    def _build_parsing_table(self):
        aug_grammar = self.G.AugmentedGrammar(True)

        # os.chdir("..")

        self.automaton = build_LR1_automaton(aug_grammar)
        for i, node in enumerate(self.automaton):
            if self.verbose:
                print(i, '\t', '\n\t '.join(str(x) for x in node.state), '\n')
            node.idx = i

        for node in self.automaton:
            idx = node.idx
            for item in node.state:
                if item.IsReduceItem:
                    prod = item.production
                    if prod.Left == aug_grammar.startSymbol:
                        self._register(self.action, (idx, aug_grammar.EOF), (SROperations.OK, None))
                    else:
                        for lookahead in item.lookaheads:
                            self._register(self.action, (idx, lookahead), (SROperations.REDUCE, prod))
                else:
                    next_symbol = item.NextSymbol
                    if next_symbol.IsTerminal:
                        self._register(self.action, (idx, next_symbol), (SROperations.SHIFT, node[next_symbol.Name][0].idx))
                    else:
                        self._register(self.goto, (idx, next_symbol), node[next_symbol.Name][0].idx)
        print("ok")
    @staticmethod
    def _register(table, key, value):
        assert key not in table or table[key] == value, 'Shift-Reduce or Reduce-Reduce conflict!!!'
        table[key] = value