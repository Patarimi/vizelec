import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


well = {"space": 10,
        "n": 2}
margin = 10

mos_d = {"y": 15, "x": 5, "finger": 6, "poly": {"ext": 10}, "active": {"ext": 10}}


def draw_mos(axis, mos: dict, offset: tuple[int, int] = (0, 0), doping: str = "n"):
    color = "green" if doping == "n" else "yellow"
    axis.add_patch(
        Rectangle(
            (offset[0], offset[1] + mos["poly"]["ext"]),
            mos["finger"] * mos["x"] + (mos["finger"]+1)*mos["active"]["ext"],
            mos["y"],
            facecolor=color,
            fill="True",
        )
    )
    for i in range(mos["finger"]):
        ax.add_patch(
            Rectangle(
                (offset[0] + (i + 1) * mos["active"]["ext"] + i * mos["x"], offset[1]),
                mos["x"],
                2*mos["poly"]["ext"]+mos["y"],
                facecolor="red",
                fill=True,
            )
        )


fig, ax = plt.subplots()
draw_mos(ax, mos_d)
draw_mos(ax, mos_d, (0, well["space"]+mos_d["y"]+2*mos_d["poly"]["ext"]), doping="p")

plt.xlim(-margin, mos_d["finger"]*mos_d["x"] + (mos_d["finger"]+1)*mos_d["active"]["ext"] + margin)
plt.ylim(-margin, well["n"] * (mos_d["y"]+2*mos_d["poly"]["ext"]) + (well["n"] - 1) * well["space"] + margin)
plt.axis("off")
plt.savefig("test.png")
