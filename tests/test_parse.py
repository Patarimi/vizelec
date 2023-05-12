import vizelec.parse as ps


def test_verilog():
    tree = ps.parse("./tests/counter.v")
    print(tree.pretty())

