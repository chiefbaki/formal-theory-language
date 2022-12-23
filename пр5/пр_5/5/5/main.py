# Annotations
from typing import Dict, Set, List, Any
# Caching
from functools import lru_cache


class Queue:
    __slots__ = ('__data',)

    def __init__(self):
        self.__data = []

    def __iter__(self):
        return iter(self.__data)

    def __contains__(self, item) -> bool:
        return item in self.__data

    def __len__(self) -> int:
        return len(self.__data)

    def __getitem__(self, index):
        return self.__data[index]

    def __repr__(self):
        return '[' + ' '.join(self.__data) + ']'

    def get(self):
        return self.__data.pop(0)

    def put(self, value: Any):
        self.__data.append(value)

    def peek(self):
        return self.__data[0]

    def empty(self) -> bool:
        return len(self.__data) == 0


class Transition:
    __slots__ = ('previous_state', 'input_character', 'next_state')

    def __init__(self, previous_state: str, input_character: str, next_state: str):
        self.previous_state = previous_state
        self.input_character = input_character
        self.next_state = next_state

    def __repr__(self):
        return f"Transition {self.previous_state} -{self.input_character}> {self.next_state}"

    def __str__(self): return self.__repr__()


class Automate:
    __slots__ = ('nodes', 'inputs', 'P', 'start_nodes', 'end_nodes')

    def __init__(self,
                 nodes: List[str] = None,
                 inputs: List[str] = None,
                 transitions: List[Transition] = None,
                 start_nodes: List[str] = None,
                 end_nodes: List[str] = None
                 ):
        self.nodes = nodes if nodes else []
        self.inputs = inputs if inputs else []
        self.P = transitions if transitions else []
        self.start_nodes = start_nodes if start_nodes else []
        self.end_nodes = end_nodes if end_nodes else []

    def __repr__(self):
        output = 'Set of states: '
        output += ', '.join(self.nodes)
        output += '\n\nInput alphabet: '
        output += ', '.join(self.inputs)
        output += '\n\nState-transitions function:\n'
        output += '\n'.join([str(i) for i in self.P])
        output += '\n\nInitial states: '
        output += ', '.join(self.start_nodes)
        output += '\n\nFinal states: '
        output += ', '.join(self.end_nodes)
        return output

    @lru_cache(maxsize=None, typed=False)
    def ways(self, node: str) -> List[Transition]:
        """ Returns list of values, that Transitioned only from previous state selected"""
        return [*filter(lambda transition: transition.previous_state == node, self.P)]

    def check_all_ways(self, nodes: str) -> Dict[str, str]:
        # Dictionary for all ways
        overall_ways: Dict[str, Set[str]] = {inp: set() for inp in self.inputs}

        for node in nodes:
            node_ways: List[Transition] = self.ways(node)
            for way in node_ways:
                overall_ways[way.input_character].add(way.next_state)

        for node, node_w in overall_ways.items():

            # Going to next node, if current is empty
            if not node_w: continue

            node_w: List[str] = list(node_w)
            node_w.sort()
            node_w: str = ''.join(node_w)
            overall_ways[node]: str = node_w

        return overall_ways

    def convert_NFA_to_DFA(self) -> 'Automate':
        new_au = Automate()
        nodes_to_check = Queue()

        for node in self.start_nodes:
            # Adding new node to queue
            nodes_to_check.put(node)

            # And to overall nodes
            new_au.nodes.append(node)

        # Solving P
        counter = 0
        while len(nodes_to_check) != counter:
            node = nodes_to_check[counter]
            values = self.check_all_ways(node)

            for input, new_node in values.items():
                new_au.P.append(Transition(node, input, new_node))

                if new_node not in nodes_to_check:

                    # Adding new node to queue
                    nodes_to_check.put(new_node)

                    # And to overall nodes
                    new_au.nodes.append(new_node)

            counter += 1

        # Solving start nodes
        new_au.start_nodes = self.start_nodes

        # Solving end nodes
        previous_end_nodes = set(self.end_nodes)
        for node in new_au.nodes:
            # Intersection between node digits and previous automate digits
            # ['1', '12', ...]
            # {'1'} + {'3'} = set()
            # {'3', '1'} + {'3'} = {'3'}
            if len({*node}.intersection(previous_end_nodes)):
                new_au.end_nodes.append(node)

        # Solving inputs
        new_au.inputs = self.inputs

        return new_au


if __name__ == '__main__':
    au_NFA = Automate(
        nodes=['1', '2', '3'],
        inputs=['a', 'b'],
        transitions=[
            Transition('1', 'a', '1'),
            Transition('1', 'a', '2'),
            Transition('1', 'b', '3'),
            Transition('2', 'a', '2'),
            Transition('2', 'b', '1'),
            Transition('2', 'b', '3'),
            Transition('3', 'a', '3'),
            Transition('3', 'b', '3')
        ],
        start_nodes=['1'],
        end_nodes=['3']
    )

    au_DFA = au_NFA.convert_NFA_to_DFA()

    print('- NFA:\n', au_NFA, '\n', sep='')
    print('- DFA:\n', au_DFA, sep='')
