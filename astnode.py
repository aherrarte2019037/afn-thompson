class ASTNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class ConcatNode(ASTNode):
    pass

class UnionNode(ASTNode):
    pass

class StarNode(ASTNode):
    pass

class PlusNode(ASTNode):
    pass

class QuestionNode(ASTNode):
    pass

class CharNode(ASTNode):
    pass

def parse_expression(expression):
    tokens = []
    for char in expression:
        if char == ' ':
            continue
        if char in {'*', '+', '?'}:
            tokens.append((char, None))
        elif char == '|':
            tokens.append(('UNION', None))
        elif char == '.':
            tokens.append(('CONCAT', None))
        elif char == '(':
            tokens.append(('LPAREN', None))
        elif char == ')':
            tokens.append(('RPAREN', None))
        else:
            tokens.append(('CHAR', char))
    return tokens

def build_ast(tokens):
    """
    Build an AST from the list of tokens.
    This is a simplified parser for regular expressions.
    """
    output_stack = []
    operator_stack = []

    def pop_operator():
        operator = operator_stack.pop()[0]
        if operator == 'UNION':
            right = output_stack.pop()
            left = output_stack.pop()
            node = UnionNode('|')
            node.left = left
            node.right = right
        elif operator == 'CONCAT':
            right = output_stack.pop()
            left = output_stack.pop()
            node = ConcatNode('.')
            node.left = left
            node.right = right
        else:
            raise ValueError(f"Unexpected operator: {operator}")
        output_stack.append(node)

    for token in tokens:
        if token[0] == 'CHAR':
            node = CharNode(token[1])
            output_stack.append(node)
        elif token[0] == 'LPAREN':
            operator_stack.append(token)
        elif token[0] == 'RPAREN':
            while operator_stack and operator_stack[-1][0] != 'LPAREN':
                pop_operator()
            operator_stack.pop()
        elif token[0] in {'UNION', 'CONCAT'}:
            while operator_stack and operator_stack[-1][0] != 'LPAREN':
                pop_operator()
            operator_stack.append(token)
        elif token[0] in {'*', '+', '?'}:
            node = output_stack.pop()
            if token[0] == '*':
                star_node = StarNode('*')
                star_node.left = node
                output_stack.append(star_node)
            elif token[0] == '+':
                plus_node = PlusNode('+')
                plus_node.left = node
                output_stack.append(plus_node)
            elif token[0] == '?':
                question_node = QuestionNode('?')
                question_node.left = node
                output_stack.append(question_node)

    while operator_stack:
        pop_operator()

    return output_stack[0] if output_stack else None

