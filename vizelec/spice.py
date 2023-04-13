import typer
import schemdraw
import schemdraw.elements as elm
import networkx as nx
import matplotlib.pyplot as plt

app = typer.Typer()

mos_port = {"drain": 0, "gate": 1, "source": 2}


@app.command("load")
def load_spice(schem: str) -> None:
    """
    Create a graph representation of the schematic given by schem.
    :param schem: path to a spice file.
    """
    netlist = nx.Graph()
    with open(schem) as f:
        for line in f.readlines():
            if line[0] in ("*", "."):
                pass
            sep = line.split(" ")
            if line[0] in ("M",):
                add_cmp(netlist, sep[0], sep[1:4])
    nx.draw_spring(netlist, with_labels=True)
    plt.show()


def add_cmp(graph: nx.Graph, cmp_name: str, ports_lst: list[str]) -> None:
    """
    update the graph with the new component
    :param ports_lst: list of the nets connected to the component.
    :param cmp_name: name of the component
    :param graph: graph to be updated
    """
    graph.add_node(cmp_name, type="cmp", style="red")
    for net in ports_lst:
        graph.add_node(net, type="net", style="blue")
        graph.add_edge(net, cmp_name)


def main(schem: str) -> None:
    """

    :param schem: Path to the spice schematic
    """
    wires = dict()
    devices = dict()
    model = dict()
    with open(schem) as f:
        for line in f.readlines():
            if line[0] in ("*", "."):
                sep = line.split(" ")
                if sep[0] == ".model":
                    model[sep[1]] = sep[2]
            if line[0] == "M":
                sep = line.split(" ")
                devices[sep[0]] = (sep[1], sep[2], sep[3])
                for i, port in enumerate(mos_port):
                    if sep[i + 1] in wires:
                        wires[sep[i + 1]][sep[0]] = (sep[5], port)
                    else:
                        wires[sep[i + 1]] = {sep[0]: (sep[5], port)}

    print(devices)
    print(model)
    print(wires)

    d = schemdraw.Drawing()
    next_net = "0"
    d += elm.GroundSignal()
    while next_net != "cc":
        next_comp = list(wires[next_net].keys())[0]
        dev_on_net = wires[next_net].pop(next_comp)
        print(dev_on_net)
        if model[dev_on_net[0]] == "nmos":
            d += elm.NFet(anchor=dev_on_net[1]).reverse().drop("drain")
        else:
            d += elm.PFet(anchor=dev_on_net[1]).reverse().drop("source")
        if dev_on_net[1] == "drain":
            next_net = devices[next_comp][2]
        else:
            next_net = devices[next_comp][0]
        wires[next_net].pop(next_comp)
    d += elm.Vdd()
    d.draw()


"""
    d = schemdraw.Drawing()
    d += elm.Dot(open=True)
    d += elm.Line(length=1)
    d.push()
    d += elm.Line(length=1).up()
    d += (M1 := elm.PFet(anchor="gate", theta=180)).flip()
    d += elm.Vdd(at=M1.source)
    d.pop()
    d += elm.Line(length=1).down()
    d += (M2 := elm.NFet(anchor="gate", theta=180).flip())
    d += elm.GroundSignal(at=M2.source)
    d += elm.Line(at=M2.drain, length=1).up()
    d.push()
    d += elm.Line(to=M1.drain, length=1)
    d.pop()
    d += elm.Line(length=1).right()
    d += elm.Dot(open=True)

    d.draw()
"""
