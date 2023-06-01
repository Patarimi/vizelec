import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import typer


app = typer.Typer()

margin = 10

rail = {"y": 5, "space": 3}


def draw_mos(axis, mos: dict, offset: tuple[int, int] = (0, 0), doping: str = "n"):
    color = "green" if doping == "n" else "yellow"
    axis.add_patch(
        Rectangle(
            (offset[0], offset[1] + mos["poly"]["ext"]),
            mos["finger"] * mos["x"] + (mos["finger"] + 1) * mos["active"]["ext"],
            mos["y"],
            facecolor=color,
            fill="True",
        )
    )
    for i in range(mos["finger"]):
        axis.add_patch(
            Rectangle(
                (offset[0] + (i + 1) * mos["active"]["ext"] + i * mos["x"], offset[1]),
                mos["x"],
                2 * mos["poly"]["ext"] + mos["y"],
                facecolor="red",
                fill=True,
            )
        )

    axis.add_patch(
        Rectangle(
            (
                offset[0],
                offset[1] - rail["y"] - rail["space"]
                if doping == "n"
                else offset[1] + mos["y"] + 2 * mos["poly"]["ext"] + rail["space"],
            ),
            mos["finger"] * mos["x"] + (mos["finger"] + 1) * mos["active"]["ext"],
            rail["y"],
            facecolor="blue",
            fill=True,
        )
    )


@app.command()
def draw_canvas(n_well_n, n_well_p, finger):
    fig, ax = plt.subplots()
    mos_d = {
        "y": 15,
        "x": 5,
        "finger": finger,
        "poly": {"ext": 10},
        "active": {"ext": 10},
    }
    well = {"space": 10, "n": n_well_n + n_well_p}  # TODO: manage well number
    draw_mos(ax, mos_d)
    draw_mos(
        ax,
        mos_d,
        (0, well["space"] + mos_d["y"] + 2 * mos_d["poly"]["ext"]),
        doping="p",
    )
    plt.xlim(
        -margin,
        mos_d["finger"] * mos_d["x"]
        + (mos_d["finger"] + 1) * mos_d["active"]["ext"]
        + margin,
    )
    plt.ylim(
        -margin,
        well["n"] * (mos_d["y"] + 2 * mos_d["poly"]["ext"])
        + (well["n"] - 1) * well["space"]
        + margin,
    )
    plt.axis("off")
    plt.show(block=False)
    plt.waitforbuttonpress()


@app.command("main")
def flow():
    finger = typer.prompt("maximum finger number", type=int)
    n_well_n = typer.prompt("number of n-well rows", type=int)
    n_well_p = typer.prompt("number of p-well rows", type=int)
    draw_canvas(n_well_n, n_well_p, finger)
