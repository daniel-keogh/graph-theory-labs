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


class Frag:
    # Start state of NFA fragment
    start = None

    # Accept state of NFA fragment
    accept = None

    # Constructor
    def __init__(self, start, accept):
        self.start = start
        self.accept = accept


myinstance = State(label="a", edges=[])
myotherinstance = State(edges=[myinstance])

myfrag = Frag(myinstance, myotherinstance)

print(myinstance.label)
print(myotherinstance.edges[0])
print(myfrag)