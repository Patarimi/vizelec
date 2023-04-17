from lark import Lark, Transformer


def parse_verilog(verilog_file: str):
    with open("vizelec/ebnf/verilog", "r") as f:
        verilog_parser = Lark(f)
    with open(verilog_file) as f:
        t = verilog_parser.parse(f.read())
    print(VerilogTransform().transform(t))
    return t


class VerilogTransform(Transformer):
    def description(self, d):
        return d
