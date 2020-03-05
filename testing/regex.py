# Classes used in Thompson's Construction.


class State:
    """A state with one or two edges, all edges labeled by label."""

    # Constructor fot the class
    def __init__(self, label=None, edges=[]):
        self.edges = edges
        self.label = label


class Fragment:
    """An NFA fragment with a start state and an accept state."""

    # Constructor
    def __init__(self, start, accept):
        self.start = start
        self.accept = accept


def compile(infix):
    """Return an NFA fragment representing the infix regular expression."""

    # Convert infix to postfix
    postfix = shunting(infix)
    # Make infix a stack of characters
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

            start = frag2.start
            accept = frag1.accept
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
        elif c == '*':
            # Pop a single fragment off the stack
            frag = nfa_stack.pop()

            # Create new start and accept states
            accept = State()
            start = State(edges=[frag.start, accept])

            # Point the arrows
            frag.accept.edges.extend([frag.start, accept])
        else:
            accept = State()
            start = State(label=c, edges=[accept])

        # Create new instance of Fragment to represent the new NFA
        newfrag = Fragment(start, accept)

        # Push the new NFA to the NFA stack
        nfa_stack.append(newfrag)

    # The postfix should be empty & the NFA stack should only have one NFA on it.
    return nfa_stack.pop()


def shunting(infix):
    """Return the infix regular express in postfix."""

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


# Add a state to a set and follow all of the e(psilon) arrows
def follow_es(state, current):
    # Only do something when we haven't already seen the state
    if state not in current:
        # Put the state itself into current
        current.add(state)

        # See whether state is labelled by e(psilon)
        if state.label is None:
            # Loop through the states pointed to by this state
            for x in state.edges:
                # Follow all of their e(psilons) too
                follow_es(x, current)


def match(regexp, s):
    """
    This function will return `True` if the regular expression `regexp` fully matches the string `s`,
    and `False` otherwise.
    """

    # Compile the regular expression into an NFA and ask the NFA if it matches the string s.
    nfa = compile(regexp)

    # Try to match the regular expression to the string s

    current = set()  # The current set of states

    # Add the first state and follow all e(psilon) arrows
    follow_es(nfa.start, current)

    previous = set()  # The previous set of states

    # Loop through characters in s
    for c in s:
        # Keep track of where we were
        previous = current
        # Create a new empty set for states we're about to be in
        current = set()

        # Loop through the previous states
        for state in previous:
            # Only follow arrows not labeled by e(psilon)
            if state.label is not None:
                # If the label equals the character we've read
                if state.label == c:
                    # Add the state at the end of the arrow to current
                    follow_es(state.edges[0], current)

    return nfa.accept in current


if __name__ == "__main__":
    tests = [
        ["a.b|b*", "bbbbbbb", True],
        ["a.b|b*", "bbbbbbbx", False],
        ["a.b",  "ab", True]
    ]

    for test in tests:
        assert match(test[0], test[1]) == test[2], test[0] + \
            (" should match " if test[2] else " should not match ") + test[1]

    # assert match("a.b|b*", "bbbbbbbb"), "a.b|b* should match bbbbbbbb"
    # assert match("a.b|b*", "xbbbbbbbb"), "a.b|b* should not match bbbbbbbb"

# print(__name__)
