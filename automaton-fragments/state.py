# Classes used in Thompson's Construction.


class State:
    # Every state has 0, 1 or 2 edges from it.
    edges = []

    # Label for the arrows. None means epsilon
    label = None

    # Constructor fot the class
    def __init__(self, label=None, edges=[]):
        self.edges = edges
        self.label = label


class Fragment:
    # Start state of NFA fragment
    start = None

    # Accept state of NFA fragment
    accept = None

    # Constructor
    def __init__(self, start, accept):
        self.start = start
        self.accept = accept


def regex_compile(infix):
    postfix = shunting(infix)
    postfix = list(postfix)[::-1]

    nfa_stack = []
    newfrag = None

    while postfix:
        # Pop a character from postfix
        c = postfix.pop()
        if c == '.':
            # Pop two fragments off the stack
            frag1 = nfa_stack.pop()
            frag2 = nfa_stack.pop()

            # Point frag2's accept state at frag1's start state
            frag2.accept.edges.append(frag1.start)

            # Create new instance of Fragment to represent the new NFA
            newfrag = Fragment(frag2.start, frag1.accept)
        elif c == '|':
            # Pop two fragments off the stack
            frag1 = nfa_stack.pop()
            frag2 = nfa_stack.pop()

            # Create new start & accept states
            accept = State()
            start = State(edges=[frag2.start, frag1.start])

            # Point the old accept states at the new one
            frag2.accept.edges.append(accept)
            frag1.accept.edges.append(accept)

            # Create new instance of Fragment to represent the new NFA
            newfrag = Fragment(start, accept)
        elif c == '*':
            # Pop a single fragment off the stack
            frag = nfa_stack.pop()

            # Create new start and accept states
            accept = State()
            start = State(edges=[frag.start, accept])

            # Point the arrows
            frag.accept.edges.extend([frag.start, accept])

            # Create new instance of Fragment to represent the new NFA
            newfrag = Fragment(start, accept)
        else:
            accept = State()
            start = State(label=c, edges=[accept])

            newfrag = Fragment(start, accept)

        # Push the new NFA to the NFA stack
        nfa_stack.append(newfrag)

    # The postfix should be empty & the NFA stack should only have one NFA on it.
    return nfa_stack.pop()


def match(regexp, s):
    """
    This function will return `True` if the regular expression `regexp` fully matches the string `s`,
    and `False` otherwise.
    """

    # Compile the regular expression into an NFA and ask the NFA if it matches the string s.
    nfa = regex_compile(regexp)
    return nfa


def shunting(infix):
    # The Shunting Yard Algorithm for regular expressions

    # Convert input to a stack-ish list
    infix = list(infix)[::-1]

    # Operator stack
    opers = []

    # Output list
    postfix = []

    # Operator precedence
    prec = {'*': 100, '.': 80, '|': 60, '(': 40, ')': 20}

    # Loop through the input one character at a time
    while infix:
        # Pop a character from the input
        c = infix.pop()

        # Decide what to do based on the character
        if c == '(':
            # Push an open bracket to the opers stack
            opers.append(c)
        elif c == ')':
            # Pop the operators stack until you find an open bracket
            while opers[-1] != '(':
                postfix.append(opers.pop())

            # Get rid of the open bracket
            opers.pop()
        elif c in prec:
            # Push any operators on the opers stack with higher prec to the output
            while opers and prec[c] < prec[opers[-1]]:
                postfix.append(opers.pop())
            # Push c to the operators stack
            opers.append(c)
        else:
            # Typically we just push the character to the output
            postfix.append(c)

    # Pop all the operators to the ouput
    while (opers):
        postfix.append(opers.pop())

    # Convert output list to a string
    postfix = "".join(postfix)
    return postfix


print(match("a.b|b*", "bbbbbbbb"))
