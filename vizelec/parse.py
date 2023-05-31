from lark import Lark, Transformer
from os.path import join, splitext


def parse(file: str):
    base_template = "vizelec/ebnf"
    _, ext = splitext(file)
    template = ""
    if ext == ".v":
        template = "verilog"
    if ext in (".cir", ".sp"):
        template = "spice"
    if template == "":
        raise ValueError(f"File extension {ext} unknown.")
    with open(join(base_template, template), "r") as f:
        verilog_parser = Lark(f)
    with open(file) as f:
        t = verilog_parser.parse(f.read())
    return t


class VerilogTransform(Transformer):
    def description(self, d):
        return d
