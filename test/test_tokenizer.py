import pypendency.lark.lexer as lexer


def test_parser():
    raw_text = " Node1 -> Node2"
    lex = lexer.Lexer()
    raw_relations = lex.parse(raw_text)
    got = raw_relations[0]
    assert len(raw_relations) == 1
    assert got.from_node.data == "node"
    assert got.edge.data == "to"
    assert got.label == ""
    assert got.to_node.data == "node"


def test_parser_for_group():
    raw_text = " Node1 -> [Node2, Node3]"
    lex = lexer.Lexer()
    raw_relations = lex.parse(raw_text)
    got = raw_relations[0]
    assert len(raw_relations) == 1
    assert got.from_node.data == "node"
    assert got.edge.data == "to"
    assert got.label == ""
    assert got.to_node.data == "node_group"

