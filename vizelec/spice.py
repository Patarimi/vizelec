import typer
import schemdraw
import schemdraw.elements as elm
import networkx as nx
import matplotlib.pyplot as plt
from .parse import parse

app = typer.Typer()

mos_port = {"drain": 0, "gate": 1, "source": 2}
letters = {'bipolar': "Q", 'resistor': "R", "mos":"M"}

@app.command("load")
def load_spice(schem: str, show: bool = True) -> None:
    """
    Create a graph representation of the schematic given by schem.
    :param schem: path to a spice file.
    :param show: display the netlist as a graph
    """
    netlist = nx.Graph()
    tree = parse(schem)
    for thing in tree.children:
        if thing.data in ("model", "v_source", "title", "instr"):
            continue
        name = letters[thing.data] + thing.children[0]
        nets = list()
        for t in thing.children:
            if t.type == "NET":
                nets.append(t.value)
        print(f"adding {name} at {nets}")
        add_cmp(netlist, name, nets)
    pos = nx.spring_layout(netlist)
    cmp_list = [n for n in netlist.nodes if netlist.nodes[n]['type'] == "cmp"]
    nx.draw_networkx(netlist, pos, with_labels=True)
    nx.draw_networkx_nodes(netlist, pos, nodelist=cmp_list, node_color="tab:red")
    if show:
        plt.show()


def add_cmp(graph: nx.Graph, cmp_name: str, ports_lst: list[str]) -> None:
    """
    update the graph with the new component
    :param ports_lst: list of the nets connected to the component.
    :param cmp_name: name of the component
    :param graph: graph to be updated
    """
    graph.add_node(cmp_name, type="cmp", node_color="tab:red")
    for net in ports_lst:
        graph.add_node(net, type="net", node_color="tab:blue")
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
