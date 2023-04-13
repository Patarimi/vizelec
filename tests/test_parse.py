import vizelec.parse as ps


def test_verilog():
    tree = ps.parse_verilog("./tests/counter.v")
    print(tree.pretty())
    assert False
