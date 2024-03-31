from common.utils import ContainerSet
from common.automata import State, multiline_formatter
from common.pycompiler import Item


def build_LR1_automaton(G):

    """
        construye el automata LR1 dado una gramatica
    """

    #ssert len(G.startSymbol.productions) == 1, 'Grammar must be augmented'
    
    start_production = G.startSymbol.productions[0]
    start_item = Item(start_production, 0, lookaheads=(G.EOF,))
    start = frozenset([start_item])
    
    closure = closure_lr1(start, G)
    automaton = State(frozenset(closure), True)
    
    pending = [ start ]
    visited = { start: automaton }
    
    while pending:
        current = pending.pop()
        current_state = visited[current]
        
        for symbol in G.terminals + G.nonTerminals:
            # Your code here!!! (Get/Build `next_state`)
            next_items = frozenset(goto_lr1(current_state.state,symbol,G))
            if not next_items:
                continue
            try:
                next_state = visited[next_items]
            except KeyError:
                visited[next_items] = State(next_items,True)
                pending.append(next_items)
                next_state = visited[next_items]
            
            current_state.add_transition(symbol.Name, next_state)
    
    automaton.set_formatter(multiline_formatter)
    return automaton


def goto_lr1(items, symbol, G, just_kernel=False):
    """
        Calcula Goto(I,X) \n
        I = items \n
        X = symbols
    """
    items = frozenset(item.NextItem() for item in items if item.NextSymbol == symbol)
    return items if just_kernel else closure_lr1(items, G)


def closure_lr1(items, G):
    """
        Calcula  CL(I) (la Clausura de I)\n
        In =  items\n
    """

    closure = ContainerSet(*items)
    
    changed = True
    while changed:
        changed = False
        
        new_items = ContainerSet()
        # Your code here!!!
        for item in closure:
            for new_item in expand(item,G):
                new_items.add(new_item)            

        changed = closure.update(new_items)
        
    return compress(closure)


def compress(items):
    centers = {}

    for item in items:
        center = item.Center()
        try:
            lookaheads = centers[center]
        except KeyError:
            centers[center] = lookaheads = set()
        lookaheads.update(item.lookaheads)
    
    return { Item(x.production, x.pos, set(lookahead)) for x, lookahead in centers.items() }


def expand(item, G):
    next_symbol = item.NextSymbol
    if next_symbol is None or not next_symbol.IsNonTerminal:
        return []
    
    lookaheads = ContainerSet()
    firsts = compute_firsts(G)
    firsts[G.EOF] = ContainerSet(G.EOF)
    
    for preview in item.Preview():
        lookaheads.update(compute_local_first(firsts,preview))        
    
    assert not lookaheads.contains_epsilon
    
    output = []
    for production in G.Productions:
        if production.Left == next_symbol:
            output.append(Item(production,0,lookaheads))
    return output

def compute_local_first(firsts, alpha):
    """
    """
    first_alpha = ContainerSet()

    try:
        alpha_is_epsilon = alpha.IsEpsilon
    except:
        alpha_is_epsilon = False

    if alpha_is_epsilon:
        first_alpha.set_epsilon()

    else:
        for symbol in alpha:
            first_alpha.update(firsts[symbol])
            if not firsts[symbol].contains_epsilon:
                break
        else:
            first_alpha.set_epsilon()

    return first_alpha


def compute_firsts(grammar):
    """
    """
    firsts = {}
    change = True

    for terminal in grammar.terminals:
        firsts[terminal] = ContainerSet(terminal)

    for non_terminal in grammar.nonTerminals:
        firsts[non_terminal] = ContainerSet()

    while change:
        change = False

        for production in grammar.Productions:
            left = production.Left
            alpha = production.Right

            first_left = firsts[left]

            try:
                first_alpha = firsts[alpha]
            except KeyError:
                first_alpha = firsts[alpha] = ContainerSet()

            local_first = compute_local_first(firsts, alpha)

            change |= first_alpha.hard_update(local_first)
            change |= first_left.hard_update(local_first)

    return firsts
