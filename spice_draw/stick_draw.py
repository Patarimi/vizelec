import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


active = {"y": 10, "dx": 15}
poly = {"x": 5, "dy": 10}
well = {"space": 10}
margin = 10

n_finger = 6
n_well = 2
mos = {
    "y": active["y"] + 2 * poly["dy"],
    "x": n_finger * poly["x"] + (n_finger + 1) * active["dx"],
}

fig, ax = plt.subplots()

ax.add_patch(
    Rectangle((0, poly["dy"]), mos["x"], active["y"], facecolor="green", fill=True)
)
ax.add_patch(
    Rectangle(
        (0, mos["y"] + well["space"] + poly["dy"]),
        mos["x"],
        active["y"],
        facecolor="yellow",
        fill=True,
    )
)
for i in range(n_finger):
    ax.add_patch(
        Rectangle(((i+1)*active["dx"]+i*poly["x"], 0), poly["x"], mos["y"], facecolor="red", fill=True)
    )
    ax.add_patch(
        Rectangle(((i+1)*active["dx"]+i*poly["x"], mos["y"] + well["space"]), poly["x"], mos["y"], facecolor="red", fill=True)
    )
plt.xlim(-margin, mos["x"] + margin)
plt.ylim(-margin, n_well * mos["y"] + (n_well - 1) * well["space"] + margin)
plt.savefig('test.png')
