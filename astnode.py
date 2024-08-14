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
    """
    Parse the regular expression string and return a list of tokens.
    This is a simplified lexer.
    """
    tokens = []
    for char in expression:
        if char in {'*', '+', '?'}:
            tokens.append((char, None))
        elif char == '|':
            tokens.append(('UNION', None))
        elif char == '.':
            tokens.append(('CONCAT', None))
        else:
            tokens.append(('CHAR', char))
    return tokens

def build_ast(tokens):
    """
    Build an AST from the list of tokens.
    This is a simplified parser for regular expressions.
    """
    stack = []
    for token in tokens:
        if token[0] == 'CHAR':
            node = CharNode(token[1])
        elif token[0] == 'CONCAT':
            right = stack.pop()
            left = stack.pop()
            node = ConcatNode('.')
            node.left = left
            node.right = right
        elif token[0] == 'UNION':
            right = stack.pop()
            left = stack.pop()
            node = UnionNode('|')
            node.left = left
            node.right = right
        elif token[0] == '*':
            left = stack.pop()
            node = StarNode('*')
            node.left = left
        elif token[0] == '+':
            left = stack.pop()
            node = PlusNode('+')
            node.left = left
        elif token[0] == '?':
            left = stack.pop()
            node = QuestionNode('?')
            node.left = left
        stack.append(node)

    return stack[0] if stack else None
