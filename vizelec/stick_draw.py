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

    def draw_mos(self, mos: dict, offset: tuple[float, float] = (0, 0), doping: str = "n"):
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
        plt.plot((x, x), y)


@app.command()
def draw_canvas(n_well_n, n_well_p, finger):
    canvas = Canvas()
    mos_d = {
        "y": 1,
        "x": 0.5,
        "finger": finger,
        "poly": {"ext": 0.5},
        "active": {"ext": 1.5},
    }
    well = {"space": 1, "n": n_well_n + n_well_p}  # TODO: manage well number
    canvas.draw_mos(mos_d, (0.25, 1))
    canvas.draw_mos(
        mos_d,
        (0.25, well["space"] + mos_d["y"] + 2 * mos_d["poly"]["ext"]+1),
        doping="p",
    )
    plt.xlim(
        -margin+0.25,
        mos_d["finger"] * mos_d["x"]
        + (mos_d["finger"] + 1) * mos_d["active"]["ext"]
        + margin+0.25,
    )
    plt.ylim(
        -margin+1,
        well["n"] * (mos_d["y"] + 2 * mos_d["poly"]["ext"])
        + (well["n"] - 1) * well["space"]
        + margin+1,
    )
    canvas.add_wire(2, (4, 6))
    canvas.add_wire(1, (0, 2))
    plt.axis("on")
    plt.grid(visible=True)
    plt.show()


@app.command("main")
def flow():
    finger = typer.prompt("maximum finger number", type=int)
    n_well_n = typer.prompt("number of n-well rows", type=int)
    n_well_p = typer.prompt("number of p-well rows", type=int)
    draw_canvas(n_well_n, n_well_p, finger)
