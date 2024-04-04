import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import typer
from typing import Tuple


app = typer.Typer()

margin = 1

rail = {"y": 1, "space": 0.5}


class Canvas:
    __a: plt.Axes

    def __init__(self):
        fig, self.__a = plt.subplots()

    def new_rect(self, origin: Tuple[float, float], width, height, color):
        self.__a.add_patch(
            Rectangle(origin, width, height, facecolor=color, fill="True")
        )

    def draw_mos(
        self, mos: dict, offset: tuple[float, float] = (0, 0), doping: str = "n"
    ):
        color = "green" if doping == "n" else "yellow"
        self.new_rect(
            (offset[0], offset[1] + mos["poly"]["ext"]),
            mos["finger"] * mos["x"] + (mos["finger"] + 1) * mos["active"]["ext"],
            mos["y"],
            color,
        )
        for i in range(mos["finger"]):
            self.new_rect(
                (offset[0] + (i + 1) * mos["active"]["ext"] + i * mos["x"], offset[1]),
                mos["x"],
                2 * mos["poly"]["ext"] + mos["y"],
                color="red",
            )

        self.new_rect(
            (
                offset[0],
                offset[1] - rail["y"] - rail["space"]
                if doping == "n"
                else offset[1] + mos["y"] + 2 * mos["poly"]["ext"] + rail["space"],
            ),
            mos["finger"] * mos["x"] + (mos["finger"] + 1) * mos["active"]["ext"],
            rail["y"],
            color="blue",
        )

    def add_wire(self, x: float | Tuple[float, float], y: float | Tuple[float, float]):
        if type(y) is tuple:
            plt.plot((x, x), y, color="blue")
        else:
            plt.plot(x, (y, y), color="lightblue")


@app.command()
def draw_canvas(n_well_n, n_well_p, finger, h_well_n, h_well_p):
    canvas = Canvas()
    nmos = {
        "y": h_well_n,
        "x": 0.5,
        "finger": finger,
        "poly": {"ext": 0.5},
        "active": {"ext": 1.5},
    }
    pmos = {
        "y": h_well_p,
        "x": 0.5,
        "finger": finger,
        "poly": {"ext": 0.5},
        "active": {"ext": 1.5},
    }
    well = {"space": 1, "n": n_well_n + n_well_p}  # TODO: manage well number
    canvas.draw_mos(nmos, (0.25, 1))
    canvas.draw_mos(
        pmos,
        (0.25, well["space"] + nmos["y"] + 2 * nmos["poly"]["ext"] + 1),
        doping="p",
    )
    plt.xlim(
        -margin + 0.25,
        nmos["finger"] * nmos["x"]
        + (nmos["finger"] + 1) * nmos["active"]["ext"]
        + margin
        + 0.25,
    )
    plt.ylim(
        -margin + 1,
        well["n"] * (nmos["y"] + 2 * nmos["poly"]["ext"])
        + (well["n"] - 1) * well["space"]
        + margin
        + 1,
    )
    canvas.add_wire(2, (4, 6))
    canvas.add_wire(1, (0, 2))
    canvas.add_wire((5, 7), 4)
    plt.axis("on")
    plt.grid(visible=True)
    plt.show()


@app.command("main")
def flow():
    finger = typer.prompt("maximum finger number", type=int)
    n_well_n = typer.prompt("number of n-well rows", type=int)
    h_well_n = typer.prompt("number of track per well rows", type=int)
    n_well_p = typer.prompt("number of p-well rows", type=int)
    h_well_p = typer.prompt("number of track per well rows", type=int)
    draw_canvas(n_well_n, n_well_p, finger, h_well_n, h_well_p)
