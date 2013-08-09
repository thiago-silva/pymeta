from pymeta.grammar import OMeta
from pymeta.builder import TreeBuilder, moduleFromGrammar
from pymeta.grammar import OMetaGrammar
from pymeta.runtime import _MaybeParseError, OMetaBase, EOFError

## parsing text...

grammar = """
start = spaces number:l operator:op number:r -> [op, l, r]
number = spaces digit+:d -> int(''.join(d))
operator = token("+") | token("-")
"""

Grammar = OMeta.makeGrammar(grammar, {})
parser = Grammar("5 + 7")
ast, err =  parser.apply("start")

print "AST: " + str(ast)

## parsing list with `ast` as input...

grammar_ast = """
start = ['+' number:a number:b] -> a + b
      | ['-' number:a number:b] -> a - b
number = :a
"""

ASTGrammar = OMetaGrammar(grammar_ast)
t = ASTGrammar.parseGrammar('SomeGrammarName', TreeBuilder)
ASTParser = moduleFromGrammar(t, 'SomeGrammarName', OMetaBase, {})
parser = ASTParser([ast])
res, err = parser.apply("start")
print "result: " + str(res)

### formating parse error
try:
    parser = Grammar("1 + a")
    ast, err =  parser.apply("start")
except Exception as err:
    print err.formatError(''.join(parser.input.data))
