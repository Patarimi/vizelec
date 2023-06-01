import vizelec.parse as ps


def test_verilog():
    tree = ps.parse("./tests/counter.v")
    print(tree.pretty())


def test_spice():
    tree = ps.parse("./tests/inv.cir")
    assert tree.children[0].data == "v_source"
    assert tree.children[1].children[0] == "in"
