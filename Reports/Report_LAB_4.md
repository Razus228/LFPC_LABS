# Convert from CFG to CNF

**Course** : Formal Languages & Finite Automata

**Author** : Mihailiuc Igor

***

## Theory

Chomsky Normal Form (CNF) is a specific form in the field of formal language theory and syntax analysis. It was introduced by Noam Chomsky, a renowned linguist and cognitive scientist, as a way to simplify the structure of context-free grammars (CFGs) while preserving their generative power. The CNF has several important properties that make it useful in various computational algorithms and theoretical analyses.

The Chomsky Normal Form consists of two main rules:

1. Rule 1: Every production rule is in one of the following forms:
   - A → BC, where A, B, and C are non-terminal symbols.
   - A → a, where A is a non-terminal symbol, and "a" is a terminal symbol.

   This rule ensures that the right-hand side of each production rule consists of either two non-terminals or one terminal symbol.

2. Rule 2: The start symbol S cannot appear on the right-hand side of any production rule, except for the production S → ε, where ε represents the empty string.

The Chomsky Normal Form provides several benefits:

1. Simplicity: By restricting the form of production rules, CNF simplifies the structure of context-free grammars. This simplification makes it easier to analyze and manipulate CFGs in various algorithms and tools.

2. Parsing Efficiency: CNF enables more efficient parsing algorithms, such as the CYK (Cocke-Younger-Kasami) algorithm. These algorithms take advantage of the restricted form to improve parsing speed and reduce computational complexity.

3. Formal Analysis: The restricted form of CNF allows for more precise formal analysis of context-free languages and grammars. Properties such as membership, emptiness, and equivalence can be more easily proven or disproven using CNF.

4. Learning and Language Acquisition: Chomsky Normal Form has also influenced theories of language acquisition and cognitive science. The simplified structure of CNF aligns with the idea that humans have innate linguistic abilities and cognitive constraints, which may aid in the learning and processing of languages.

Overall, Chomsky Normal Form provides a useful framework for understanding and working with context-free grammars, facilitating efficient parsing algorithms and supporting theoretical analyses in the field of formal language theory.

***

## Objectives
- Learn about Chomsky Normal Form (CNF).
- Get familiar with the approaches of normalizing a grammar.
- Implement a method for normalizing an input grammar by the rules of CNF

***

## Implementation description

The first step for converting CFG to CNF is to remove all **epsylon** productions. 

Firstly, the function iterates over the CFG to see if there are any nullable non-terminals: 
```
nullable = set()
    while True:
        new_nullable = set()
        for nt in cfg['nonterminals']:
            if '' in cfg['productions'][nt] or any(all(symbol in nullable for symbol in prod) for prod in cfg['productions'][nt]):
                new_nullable.add(nt)
        if new_nullable == nullable:
            break
        nullable = new_nullable
```

Then if it finds if there are any **epsylon** productions, it starts removing those productions: 
```
new_productions = {}
    for nt, prods in cfg['productions'].items():
        new_prods = set()
        for prod in prods:
            if prod == '':
                continue
            for combination in product(*[nullable if symbol == nt else [symbol] for symbol in prod]):
                new_prods.add(''.join(combination))
        new_productions[nt] = new_prods
```

Lastly it creates a new directory for the cfg: 
```
new_cfg = {
        'start_symbol': cfg['start_symbol'],
        'nonterminals': cfg['nonterminals'],
        'terminals': cfg['terminals'],
        'productions': new_productions
    }

    return new_cfg
```

The next step is to remove all renamings. The code checks if there are any renamings: 
```
terminals_only = set()
    for nt in cfg['nonterminals']:
        if len(cfg['productions'][nt]) == 1 and \
           cfg['productions'][nt].pop().islower():
            terminals_only.add(nt)
```
Then if it finds them, it removes them: 
```
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
```

Lastly, it updates the directory from the epsylon function. Next step is to eliminate inaccesible symbols: 
```
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
```

The last step is to eliminate non-productive symbols. 
```
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
```

The final function for converting from CFG to CNF is the **convert_to_chomsky_normal_form** function itself.

The code for it is: 
```
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
```

To test it, my variant is: 
```
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
```

## Results
The code seems to not work as it is supposed to. The output I get is meaningless, and I tried to fix the error, but didn't manage to. Here is the output:
```
{'start_symbol': 'S', 'nonterminals': set(), 'terminals': {'b', 'd', 'a'}, 'productions': {}}
```

## Conclusion

In conclusion, converting a Context-Free Grammar (CFG) to Chomsky Normal Form (CNF) holds significant importance in the field of formal language theory and syntax analysis. The conversion process simplifies the structure of CFGs while preserving their generative power, leading to several practical and theoretical benefits.

Firstly, converting CFGs to CNF simplifies their structure, making them easier to analyze and manipulate. The restricted form of CNF allows for more efficient parsing algorithms, enabling faster processing and reduced computational complexity. This is particularly useful in applications such as natural language processing, where parsing large amounts of text or speech is required.

Secondly, CNF facilitates formal analysis of context-free languages and grammars. The restricted form allows for more precise proofs and disproofs of properties like membership, emptiness, and equivalence. This enhances our understanding of the expressive power and limitations of context-free grammars.

Furthermore, the conversion to CNF has implications for theories of language acquisition and cognitive science. The simplified structure aligns with the idea that humans have innate linguistic abilities and cognitive constraints, aiding in the learning and processing of languages. By studying CNF representations, researchers can gain insights into how languages are acquired and processed by individuals.

Overall, converting CFGs to Chomsky Normal Form is crucial for efficient parsing, formal analysis, and advancing our understanding of language and cognition. It provides a standardized and simplified representation that enables practical applications and theoretical investigations in the field of formal language theory.

## References
1. https://en.wikipedia.org/wiki/Chomsky_normal_form
2. https://www.geeksforgeeks.org/converting-context-free-grammar-chomsky-normal-form/