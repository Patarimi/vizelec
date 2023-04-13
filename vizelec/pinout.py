import typer
import schemdraw as sd
import schemdraw.elements as elm

app = typer.Typer()

map_pin = {"W": "left", "E": "right", "S": "bott", "N": "top"}


@app.command("show")
def show_pin_order(conf_file: str):
    pin_list = read_conf(conf_file)
    pins = (elm.IcPin(name=name, side=side, rotation=0 if side in ("left", "right") else 90) for name, side in pin_list)
    schem = sd.Drawing()
    schem += elm.Ic(pins=pins)
    schem.draw()
    return


def read_conf(conf_file: str):
    current_dir = ""
    pin_list = list()
    with open(conf_file) as f:
        for line in f.readlines():
            if line[0] == "#":
                if line[1] in map_pin.keys():
                    current_dir = map_pin[line[1]]
            else:
                pin_list.append((line, current_dir))
    return pin_list
