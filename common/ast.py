import common.visitor as visitor
from typing import List, Union

'''
-Node
    -ProgramNode
    -ParameterNode
    -TypeAtributeNode
    -ProtocolMethodNode
    -StatementNode
        -FunctionNode
        -TypeNode
        -ProtocolNode
    -ExpressionNode
        -ExpressionBlockNode
        
            ___(Less Priority)___
            -LetNode
            -IfElseExpression
            -DestructiveExpression
            -SelfDestructiveExpression
            -WhileNode
            -ForNode
            -NewNode
            
            ___(Operations)___
            -OrAndExpression
            -NotExpression
            -ComparationExpression
            -IsExpression
            -StringConcatenationNode
            -AritmethicExpression
            
            __(High Priority)__
            -NumberNode
            -StringNode
            -BooleanNode
            -VariableNode
            -SelfVariableNode
            -FunctionCallNode
            -TypeFunctionCallNode
            -ListNode
            -ImplicitListNode
            -InexingNode
            -asNode
'''


class node:
    """
        Basic node class. The building block of the AST
    """
    pass


class StatementNode(node):
    """
        A statement can be a Type definition, a method declaration, an expression or a protocol
    """
    pass


class ExpressionNode(StatementNode):
    '''
        An expression in HULK is anything that has a value
    '''

    def __init__(self):
        self.VALUE_TYPE = 'Object'
        pass


class ProgramNode(node):
    '''
        A program in HULK is a collection of statements
    '''

    def __init__(self, statements: list[StatementNode], expression: ExpressionNode):
        self.STATEMENTS = statements
        self.EXPRESSION = expression


class ParameterNode(node):
    '''
        Represents a parameter for a function/method, a constructor for a Type or a let expression
        A parameter must have a name, and the Type can be specified
    '''

    def __init__(self, name: str, type: str = 'Object'):
        self.NAME = name
        self.TYPE = type


class FunctionNode(StatementNode):
    '''
        This contains a declaration of a function.
        A function needs a name and an expression.
        And it may contain parameters and a return Type
    '''

    def __init__(self, name: str, parameters: list[ParameterNode],
                 corpus: ExpressionNode, type: str = 'Object'):
        self.NAME = name
        self.PARAMETERS = parameters
        self.CORPUS = corpus
        self.TYPE = type


class TypeAtributeNode(node):
    '''
        This is an atribute of a class. It has a name and a value from a expression
    '''

    def __init__(self, param: ParameterNode, value: ExpressionNode):
        self.VAR = param
        self.VALUE = value


class TypeNode(StatementNode):
    '''
        This contains a class declaration.
        Contains a name and a corpus.
        It may have a constructor and a parent in hierarchy
        In case of hierarchy, you can call arguments for the parent
    '''

    def __init__(self, name: str, corpus: list[Union[FunctionNode, TypeAtributeNode]]
                 , parameters: list[ParameterNode] = [], inherits: str = "Object",
                 arguments: list[ExpressionNode] = []):
        self.NAME = name
        self.CORPUS = corpus
        self.CONSTRUCTOR = parameters
        self.INHERITS = inherits
        self.ARGUMENTS = arguments


class ProtocolMethodNode(node):
    '''
        This is a abstract method inside of a protocol.
        Needs to have a name, a Type and a Typed Parameter List
    '''

    def __init__(self, name: str, parameters: List[ParameterNode], type: str):
        self.NAME = name
        self.PARAMETERS = parameters
        self.TYPE = type


class ProtocolNode(StatementNode):
    '''
        This is a protocol. It has a name and and a list of fully-Typed methods.
        A protocol may extend another protocol
    '''

    def __init__(self, name: str, corpus: List[ProtocolMethodNode], extends: str = ''):
        self.NAME = name
        self.CORPUS = corpus
        self.EXTENDS = extends


class ExpressionBlockNode(ExpressionNode):
    '''
        This node represents a list of Expressions joined together.
    '''

    def __init__(self, expressions: List[ExpressionNode]):
        self.EXPRESSIONS = expressions
        self.VALUE_TYPE = 'Object'

class LetNode(ExpressionNode):
    '''
        Contains a Let expression. Contains a list of variables,
        his corresponding expressions for his values and the expression to aplied
    '''

    def __init__(self, variable_names: List[ParameterNode],
                 variable_values: List[ExpressionNode],
                 expression: ExpressionNode):
        self.VARS = variable_names
        self.VAR_VALUES = variable_values
        self.EXPRESSION = expression
        self.VALUE_TYPE = 'Object'


class IfElseExpression(ExpressionNode):
    '''
        Contains the semantic of the conditionals.
        It has a list of conditions (the condition of the if, 
            then the condition of the first elif...)
        And a list of expression (the if case, the first elif case... and the else case)
    '''

    def __init__(self, conditions: List[ExpressionNode], expressions: List[ExpressionNode]):
        self.CONDITIONS = conditions
        self.CASES = expressions
        self.VALUE_TYPE = 'Object'


class DestructiveExpression(ExpressionNode):
    '''
        This contains the semantic for := operator.
        It has the varible name and the Expression.
    '''

    def __init__(self, name: str, expression: ExpressionNode):
        self.NAME = name
        self.EXPRESSION = expression
        self.VALUE_TYPE = 'Object'


class SelfVariableNode(ExpressionNode):
    '''
        The call of an atribute inside a class
    '''

    def __init__(self, is_self: bool, name: str):
        self.IS_SELF = is_self
        self.NAME = name
        self.VALUE_TYPE = 'Object'


class SelfDestructiveExpression(ExpressionNode):
    '''
        This is contains the semantic for := operator on the case that is for an attribute of a type
    '''

    def __init__(self, var: SelfVariableNode, expression: ExpressionNode):
        self.VAR = var
        self.EXPRESSION = expression
        self.VALUE_TYPE = 'Object'


class WhileNode(ExpressionNode):
    '''
        Has the semantic for a while cicle. Contains the condition and the expressions
    '''

    def __init__(self, condition: ExpressionNode, expression: ExpressionNode):
        self.CONDITIONS = condition
        self.EXPRESSION = expression
        self.VALUE_TYPE = 'Object'


class ForNode(ExpressionNode):
    '''
        Has the semantic for a for cicle. Contains the colection, the iterator and the expressions
    '''

    def __init__(self, name: str, collection: ExpressionNode, expression: ExpressionNode):
        self.NAME = name
        self.COLLECTION = collection
        self.EXPRESSION = expression
        self.VALUE_TYPE = 'Object'


class NewNode(ExpressionNode):
    '''
        Contains the new operator. Contains the name of a Type and the constructor arguments
    '''

    def __init__(self, name: str, arguments: List[ExpressionNode]):
        self.NAME = name
        self.ARGS = arguments
        self.VALUE_TYPE = 'Object'


class OrAndExpression(ExpressionNode):
    '''
        Contains the operators &, |.
    '''

    def __init__(self, operation: str, left: ExpressionNode, right: ExpressionNode):
        self.LEFT = left
        self.RIGHT = right
        self.OPERATION = operation
        self.VALUE_TYPE = 'Object'


class NotExpression(ExpressionNode):
    '''
        Contains the operator !.
    '''

    def __init__(self, expression: ExpressionNode):
        self.EXPRESSION = expression
        self.VALUE_TYPE = 'Object'


class ComparationExpression(ExpressionNode):
    '''
        Contains the operators >, <, <=, >=, ==. Recive 2 expressions and compares them
    '''

    def __init__(self, operation: str, left: ExpressionNode, right: ExpressionNode = None):
        self.LEFT = left
        self.RIGHT = right
        self.OPERATION = operation
        self.VALUE_TYPE = 'Object'


class IsExpression(ExpressionNode):
    '''
        Contains the operator is
    '''

    def __init__(self, left: ExpressionNode, name: str):
        self.LEFT = left
        self.NAME = name
        self.VALUE_TYPE = 'Object'


class StringConcatenationNode(ExpressionNode):
    '''
        Contains the @ and @@ operators
    '''

    def __init__(self, left: ExpressionNode
                 , right: ExpressionNode, double: bool = False):
        self.LEFT = left
        self.RIGHT = right
        self.DOUBLE = double
        self.VALUE_TYPE = 'Object'


class ArithmeticExpression(ExpressionNode):
    '''
        Contains all the arithmetic expressions:
        + - * ** ^ / %
        The unary expression -Expression is included has 0-Expression
    '''

    def __init__(self, operation: str, left: ExpressionNode
                 , right: ExpressionNode):
        self.LEFT = left
        self.RIGHT = right
        self.OPERATION = operation
        self.VALUE_TYPE = 'Object'


class AsNode(ExpressionNode):
    '''
        as operator
    '''

    def __init__(self, left: ExpressionNode, right: str):
        self.EXPRESSION = left
        self.TYPE = right
        self.VALUE_TYPE = 'Object'


class NumberNode(ExpressionNode):
    '''
        Contains a number value
    '''

    def __init__(self, value):
        self.VALUE = value
        self.VALUE_TYPE = 'Object'


class StringNode(ExpressionNode):
    '''
        Contains a string value
    '''

    def __init__(self, value):
        self.VALUE = value
        self.VALUE_TYPE = 'Object'


class BooleanNode(ExpressionNode):
    '''
        True or False
    '''

    def __init__(self, value):
        self.VALUE = value
        self.VALUE_TYPE = 'Object'


class VariableNode(ExpressionNode):
    '''
        A variable
    '''

    def __init__(self, name: str):
        self.NAME = name
        self.VALUE_TYPE = 'Object'


class FunctionCallNode(ExpressionNode):
    '''
        A function call. Recieves a name and arguments
    '''

    def __init__(self, name: str, arguments: List[ExpressionNode]):
        self.FUNCT = name
        self.ARGS = arguments
        self.VALUE_TYPE = 'Object'


class TypeFunctionCallNode(ExpressionNode):
    '''
        The combination of the last two
    '''

    def __init__(self, class_calling: ExpressionNode, name: str, arguments: List[ExpressionNode]):
        self.CLASS = class_calling
        self.FUNCT = name
        self.ARGS = arguments
        self.VALUE_TYPE = 'Object'


class ListNode(ExpressionNode):
    '''
        Represents a list in code. It receives an array with its elements
    '''

    def __init__(self, expressions: List[ExpressionNode]):
        self.ELEMENTS = expressions
        self.VALUE_TYPE = 'Object'


class ImplicitListNode(ExpressionNode):
    '''
        This is for a implicit list.
        The operator is an operation to do to each element of a collection
        The iterator is the name of a element from the collection in the operator
    '''

    def __init__(self, operator: ExpressionNode, iterator: str, collection: ExpressionNode):
        self.OPERATION = operator
        self.ITERATION = iterator
        self.COLLECTION = collection
        self.VALUE_TYPE = 'Object'


class IndexingNode(ExpressionNode):
    '''
        This  node represents an indexing on a object
    '''

    def __init__(self, collection: ExpressionNode, index: ExpressionNode):
        self.COLLECTION = collection
        self.INDEX = index
        self.VALUE_TYPE = 'Object'