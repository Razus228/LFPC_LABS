from itertools import product

cfg = {
    'start_symbol': 'S',
    'nonterminals': {'S', 'A', 'B', 'C'},
    'terminals': {'a', 'b', 'd'},
    'productions': {
        'S': {'dB', 'A'},
        'A': {'d', 'dS', 'aBdAB'},
        'B': {'a', 'dA', 'A', ''},
        'C': {'Aa'}
    }
}

def eliminate_epsilon(cfg):
    """
    Eliminates all epsilon productions from a context-free grammar.

    Args:
        cfg (dict): A dictionary representing the context-free grammar.

    Returns:
        A new dictionary representing the context-free grammar with all epsilon productions removed.
    """
    # Find all nullable nonterminals
    nullable = set()
    while True:
        new_nullable = set()
        for nt in cfg['nonterminals']:
            if '' in cfg['productions'][nt] or any(all(symbol in nullable for symbol in prod) for prod in cfg['productions'][nt]):
                new_nullable.add(nt)
        if new_nullable == nullable:
            break
        nullable = new_nullable

    # Remove all epsilon productions
    new_productions = {}
    for nt, prods in cfg['productions'].items():
        new_prods = set()
        for prod in prods:
            if prod == '':
                continue
            for combination in product(*[nullable if symbol == nt else [symbol] for symbol in prod]):
                new_prods.add(''.join(combination))
        new_productions[nt] = new_prods

    # Create the new CFG dictionary
    new_cfg = {
        'start_symbol': cfg['start_symbol'],
        'nonterminals': cfg['nonterminals'],
        'terminals': cfg['terminals'],
        'productions': new_productions
    }

    return new_cfg

def eliminate_renamings(cfg):
    """
    Eliminates renamings from a context-free grammar.

    Args:
        cfg (dict): A dictionary representing the context-free grammar.

    Returns:
        A new dictionary representing the context-free grammar with renamings eliminated.
    """
    # First, find all nonterminals that can derive only terminals
    terminals_only = set()
    for nt in cfg['nonterminals']:
        if len(cfg['productions'][nt]) == 1 and \
           cfg['productions'][nt].pop().islower():
            terminals_only.add(nt)

    # Now, eliminate all renamings
    new_productions = {}
    for nt in cfg['nonterminals']:
        new_productions[nt] = set()
        for prod in cfg['productions'][nt]:
            if prod.islower() or prod in terminals_only:
                # This is either a terminal or a nonterminal that only derives terminals,
                # so we can just add it directly to the new productions
                new_productions[nt].add(prod)
            else:
                # This is a nonterminal that can derive nonterminals, so we need to
                # replace it with its productions
                for symbol in prod:
                    if symbol in terminals_only:
                        # This is a nonterminal that only derives terminals, so we can
                        # add its productions directly
                        new_productions[nt].update(cfg['productions'][symbol])
                    elif symbol.isupper():
                        # This is a nonterminal that can derive nonterminals, so we need
                        # to add all of its productions (except for itself)
                        for prod2 in cfg['productions'][symbol]:
                            if prod2 != symbol:
                                new_productions[nt].add(prod2)

    # Return the updated CFG
    return {'start_symbol': cfg['start_symbol'],
            'nonterminals': cfg['nonterminals'] - terminals_only,
            'terminals': cfg['terminals'],
            'productions': new_productions}



def eliminate_inaccessible(cfg):
    """
    Eliminates all inaccessible nonterminals and their productions from a context-free grammar.

    Args:
        cfg (dict): A dictionary representing the context-free grammar.

    Returns:
        A new dictionary representing the context-free grammar with all inaccessible nonterminals and their productions removed.
    """
    # Find all reachable nonterminals starting from the start symbol
    reachable = set()
    frontier = set([cfg['start_symbol']])
    while frontier:
        nt = frontier.pop()
        reachable.add(nt)
        for prod in cfg['productions'][nt]:
            for symbol in prod:
                if symbol in cfg['nonterminals'] and symbol not in reachable:
                    frontier.add(symbol)

    # Remove all nonterminals and their productions that are not reachable
    new_productions = {}
    for nt in reachable:
        new_productions[nt] = set()
        for prod in cfg['productions'][nt]:
            if all(symbol in reachable or symbol == '' for symbol in prod):
                new_productions[nt].add(prod)

    # Remove all nonterminals that are not reachable
    new_nonterminals = reachable.intersection(cfg['nonterminals'])

    # Create the new CFG dictionary
    new_cfg = {
        'start_symbol': cfg['start_symbol'],
        'nonterminals': new_nonterminals,
        'terminals': cfg['terminals'],
        'productions': new_productions
    }

    return new_cfg


def eliminate_nonproductive(cfg):
    """
    Eliminates all non-productive nonterminals and their productions from a context-free grammar.

    Args:
        cfg (dict): A dictionary representing the context-free grammar.

    Returns:
        A new dictionary representing the context-free grammar with all non-productive nonterminals and their productions removed.
    """
    # Find all productive nonterminals
    productive = set()
    while True:
        new_productive = set()
        for nt in cfg['nonterminals']:
            if any(all(symbol in productive or symbol == '' for symbol in prod) for prod in cfg['productions'][nt]):
                new_productive.add(nt)
        if new_productive == productive:
            break
        productive = new_productive

    # Remove all nonterminals and their productions that are not productive
    new_productions = {}
    for nt in productive:
        new_productions[nt] = set()
        for prod in cfg['productions'][nt]:
            if all(symbol in productive or symbol == '' for symbol in prod):
                new_productions[nt].add(prod)

    # Remove all nonterminals that are not productive
    new_nonterminals = productive.intersection(cfg['nonterminals'])

    # Create the new CFG dictionary
    new_cfg = {
        'start_symbol': cfg['start_symbol'],
        'nonterminals': new_nonterminals,
        'terminals': cfg['terminals'],
        'productions': new_productions
    }

    return new_cfg


def convert_to_chomsky_normal_form(cfg):
    """
    Converts a context-free grammar to Chomsky normal form.

    Args:
        cfg (dict): A dictionary representing the context-free grammar.

    Returns:
        A new dictionary representing the context-free grammar in Chomsky normal form.
    """
    # Step 1: Eliminate ε-productions
    cfg = eliminate_epsilon(cfg)

    # Step 2: Eliminate unit productions
    cfg = eliminate_renamings(cfg)

    # Step 3: Eliminate non-productive nonterminals and productions
    cfg = eliminate_inaccessible(cfg)

    # Step 4: Eliminate inaccessible nonterminals and productions
    cfg = eliminate_nonproductive(cfg)

    # Step 5: Replace terminals in productions with new nonterminals
    new_productions = {}
    new_nonterminals = set()
    terminal_productions = {}
    for nt in cfg['nonterminals']:
        new_productions[nt] = set()
        for prod in cfg['productions'][nt]:
            if len(prod) > 1:
                new_productions[nt].add(prod)
            else:
                symbol = prod[0]
                if symbol in cfg['terminals']:
                    if symbol not in terminal_productions:
                        terminal_nt = f"T_{symbol}"
                        terminal_productions[symbol] = terminal_nt
                        new_nonterminals.add(terminal_nt)
                        new_productions[terminal_nt] = {symbol}
                    new_productions[nt].add(terminal_productions[symbol])
                else:
                    new_productions[nt].add(prod)

    # Step 6: Replace long productions with new nonterminals
    while True:
        new_nt_productions = {}
        for nt in cfg['nonterminals']:
            new_nt_productions[nt] = set()
            for prod in new_productions[nt]:
                if len(prod) > 2:
                    first_symbol = prod[0]
                    rest = prod[1:]
                    new_nt = f"N_{nt}"
                    new_nonterminals.add(new_nt)
                    new_nt_productions[new_nt] = {first_symbol}
                    new_nt_productions[nt].add((first_symbol, new_nt))
                    while len(rest) > 2:
                        first_symbol = new_nt
                        rest, next_symbol = rest[1:], rest[0]
                        new_nt = f"N_{nt}"
                        new_nonterminals.add(new_nt)
                        new_nt_productions[new_nt] = {next_symbol}
                        new_nt_productions[first_symbol].add((next_symbol, new_nt))
                    new_nt_productions[nt].add((rest[0], rest[1]))
                else:
                    new_nt_productions[nt].add(prod)
        if new_nt_productions == new_productions:
            break
        new_productions = new_nt_productions

    # Create the new CFG dictionary
    new_cfg = {
        'start_symbol': cfg['start_symbol'],
        'nonterminals': cfg['nonterminals'].union(new_nonterminals),
        'terminals': cfg['terminals'],
        'productions': new_productions
    }

    return new_cfg

new_cfg = convert_to_chomsky_normal_form(cfg)
print(new_cfg)



