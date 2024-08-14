import graphviz
from astnode import CharNode, ConcatNode, PlusNode, QuestionNode, StarNode, UnionNode, parse_expression, build_ast

class State:
    def __init__(self, id):
        self.id = id
        self.transitions = {}
        self.is_accept = False

    def add_transition(self, symbol, state):
        if symbol in self.transitions:
            self.transitions[symbol].append(state)
        else:
            self.transitions[symbol] = [state]

class NFA:
    def __init__(self, start_state, accept_state):
        self.start_state = start_state
        self.accept_state = accept_state
        self.states = set()

    def add_state(self, state):
        self.states.add(state)

class ThompsonConstruction:
    def __init__(self):
        self.state_id = 0

    def create_state(self):
        state = State(self.state_id)
        self.state_id += 1
        return state

    def build(self, ast_node):
        if isinstance(ast_node, CharNode):
            start = self.create_state()
            end = self.create_state()
            start.add_transition(ast_node.value, end)
            nfa = NFA(start, end)
            nfa.add_state(start)
            nfa.add_state(end)
            return nfa
        elif isinstance(ast_node, ConcatNode):
            left_nfa = self.build(ast_node.left)
            right_nfa = self.build(ast_node.right)
            left_nfa.accept_state.add_transition(None, right_nfa.start_state)
            left_nfa.accept_state.is_accept = False
            nfa = NFA(left_nfa.start_state, right_nfa.accept_state)
            nfa.states = left_nfa.states.union(right_nfa.states)
            return nfa
        elif isinstance(ast_node, UnionNode):
            start = self.create_state()
            end = self.create_state()
            left_nfa = self.build(ast_node.left)
            right_nfa = self.build(ast_node.right)
            start.add_transition(None, left_nfa.start_state)
            start.add_transition(None, right_nfa.start_state)
            left_nfa.accept_state.add_transition(None, end)
            right_nfa.accept_state.add_transition(None, end)
            left_nfa.accept_state.is_accept = False
            right_nfa.accept_state.is_accept = False
            nfa = NFA(start, end)
            nfa.states = {start, end}.union(left_nfa.states).union(right_nfa.states)
            return nfa
        elif isinstance(ast_node, StarNode):
            start = self.create_state()
            end = self.create_state()
            nfa = self.build(ast_node.left)
            start.add_transition(None, nfa.start_state)
            start.add_transition(None, end)
            nfa.accept_state.add_transition(None, nfa.start_state)
            nfa.accept_state.add_transition(None, end)
            nfa.accept_state.is_accept = False
            nfa = NFA(start, end)
            nfa.states = {start, end}.union(nfa.states)
            return nfa
        elif isinstance(ast_node, PlusNode):
            start = self.create_state()
            end = self.create_state()
            nfa = self.build(ast_node.left)
            start.add_transition(None, nfa.start_state)
            nfa.accept_state.add_transition(None, nfa.start_state)
            nfa.accept_state.add_transition(None, end)
            nfa.accept_state.is_accept = False
            nfa = NFA(nfa.start_state, end)
            nfa.states = {start, end}.union(nfa.states)
            return nfa
        elif isinstance(ast_node, QuestionNode):
            start = self.create_state()
            end = self.create_state()
            nfa = self.build(ast_node.left)
            start.add_transition(None, nfa.start_state)
            start.add_transition(None, end)
            nfa.accept_state.add_transition(None, end)
            nfa.accept_state.is_accept = False
            nfa = NFA(start, end)
            nfa.states = {start, end}.union(nfa.states)
            return nfa

def simulate_nfa(nfa, string):
    current_states = set()
    next_states = set()

    def add_state(state, visited):
        if state in visited:
            return
        visited.add(state)
        current_states.add(state)
        if None in state.transitions:
            for next_state in state.transitions[None]:
                add_state(next_state, visited)

    visited = set()
    add_state(nfa.start_state, visited)

    for char in string:
        for state in current_states:
            if char in state.transitions:
                for next_state in state.transitions[char]:
                    next_states.add(next_state)
        
        current_states = next_states
        next_states = set()
        
        visited = set()
        for state in list(current_states):
            add_state(state, visited)
        
        if not current_states:
            return False

    is_accepted = nfa.accept_state in current_states
    
    return is_accepted

def read_input(file_path):
    with open(file_path, 'r') as file:
        expressions = file.readlines()
    return [expr.strip() for expr in expressions]

def visualize_nfa(nfa, file_name):
    dot = graphviz.Digraph(comment='NFA')
    for state in nfa.states:
        shape = 'doublecircle' if state.is_accept else 'circle'
        dot.node(str(state.id), shape=shape)

    for state in nfa.states:
        for symbol, end_states in state.transitions.items():
            for end_state in end_states:
                dot.edge(str(state.id), str(end_state.id), label=symbol if symbol is not None else 'ε')
    
    dot.render(file_name, format='png', cleanup=True)

def main():
    expressions = read_input('input.txt')
    
    for i, expression in enumerate(expressions):
        ast = build_ast(parse_expression(expression))
        nfa = ThompsonConstruction().build(ast)
        nfa_file_name = f'nfa_results/nfa_{i+1}'
        visualize_nfa(nfa, nfa_file_name)
        
        test_string = input(f'Test string for"{expression}": ')
        
        result = simulate_nfa(nfa, test_string)
        print(f'Regex: {expression}, Test String: {test_string}, Accepted: {"Yes" if result else "No"}\n')

if __name__ == '__main__':
    main()
