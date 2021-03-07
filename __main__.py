import logging
from lark import Lark, logger

logger.setLevel(logging.DEBUG)

collision_grammar = '''

start: graph
graph : node (edge node|node_group)*
node_group: "["node+"]"
node: STRING
edge: "-"STRING?">"  -> to
    | "<"STRING?"-" -> from
STRING: /\w/+
%import common.WS
%ignore WS
%import common.WS_INLINE
%ignore WS_INLINE
'''

p = Lark(collision_grammar, debug=True)


text = "Eikon -feeds> DMP -hosts> feed <likes- Martin"
r = p.parse(text)
print(r.pretty())
