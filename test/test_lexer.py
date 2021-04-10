import pytest
from pypendency.lexer.lark import  core as lexer


def test_lexer():
    raw_text = " Node1 --> Node2"
    lex = lexer.Lexer()
    raw_relations = lex.parse(raw_text)
    got = raw_relations[0]
    pytest.assume(len(raw_relations) == 1)
    pytest.assume(got.from_node.data == "node")
    pytest.assume(got.edge.data == "to")
    pytest.assume(got.label == "")
    pytest.assume(got.to_node.data == "node")


def test_lexer_label():
    raw_text = " Node1 -Depends-> Node2"
    lex = lexer.Lexer()
    raw_relations = lex.parse(raw_text)
    got = raw_relations[0]
    pytest.assume(len(raw_relations) == 1)
    pytest.assume(got.from_node.data == "node")
    pytest.assume(got.edge.data == "to")
    pytest.assume(got.label == "Depends")
    pytest.assume(got.to_node.data == "node")


def test_lexer_short_notation():
    raw_text = " Node1 -> Node2"
    lex = lexer.Lexer()
    raw_relations = lex.parse(raw_text)
    got = len(raw_relations)
    want = 1
    pytest.assume( got == want)


def test_lexer_for_group():
    raw_text = " Node1 -> [Node2, Node3]"
    lex = lexer.Lexer()
    raw_relations = lex.parse(raw_text)
    got = raw_relations[0]
    pytest.assume(len(raw_relations) == 1)
    pytest.assume(got.from_node.data == "node")
    pytest.assume(got.edge.data == "to")
    pytest.assume(got.label == "")
    pytest.assume(got.to_node.data == "node_group")


def test_lexer_tripple():
    raw_text = " Node1 -> Node2 -> Node3"
    lex = lexer.Lexer()
    raw_relations = lex.parse(raw_text)
    got_1 = raw_relations[0]
    got_2 = raw_relations[1]
    pytest.assume(len(raw_relations) == 2)

    pytest.assume(got_1.from_node.data == "node")
    pytest.assume(got_1.from_node.children[0].value == "Node1")
    pytest.assume(got_1.to_node.data == "node")
    pytest.assume(got_1.to_node.children[0].value == "Node2")
    pytest.assume(got_1.edge.data == "to")
    pytest.assume(got_1.label == "")

    pytest.assume(got_2.from_node.data == "node")
    pytest.assume(got_2.from_node.children[0].value == "Node2")
    pytest.assume(got_2.to_node.data == "node")
    pytest.assume(got_2.to_node.children[0].value == "Node3")
    pytest.assume(got_2.edge.data == "to")
    pytest.assume(got_2.label == "")

def test_lexer_tripple_binarie():
    raw_text = " Node1 -Depends-> Node2 <-Depends- Node3"
    lex = lexer.Lexer()
    raw_relations = lex.parse(raw_text)
    got_1 = raw_relations[0]
    got_2 = raw_relations[1]

    pytest.assume(len(raw_relations) == 2)

    pytest.assume(got_1.from_node.data == "node")
    pytest.assume(got_1.from_node.children[0].value == "Node1")
    pytest.assume(got_1.to_node.data == "node")
    pytest.assume(got_1.to_node.children[0].value == "Node2")
    pytest.assume(got_1.edge.data == "to")
    pytest.assume(got_1.label == "Depends")

    pytest.assume(got_2.from_node.data == "node")
    pytest.assume(got_2.from_node.children[0].value == "Node2")
    pytest.assume(got_2.to_node.data == "node")
    pytest.assume(got_2.to_node.children[0].value == "Node3")
    pytest.assume(got_2.edge.data == "from")
    pytest.assume(got_2.label == "Depends")
