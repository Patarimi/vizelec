import pixie


active = {"width": 10, "length_ext": 10}
poly = {"length": 10, "width_ext": 10}
well = {"space": 10}
margin = 10

n_finger = 6
n_well = 2
mos = {"width": active["width"]+2*poly["width_ext"], "length":poly["length"]+2*active["length_ext"]}

mos_tot = (n_finger*mos["length"], n_well*mos["width"])
image = pixie.Image(mos_tot[0]+2*margin, mos_tot[1]+2*margin)
image.fill(pixie.Color(1, 1, 1, 1))

active_p = pixie.Paint(pixie.SOLID_PAINT)
active_p.color = pixie.Color(1, 1, 0, 1)

active_n = pixie.Paint(pixie.SOLID_PAINT)
active_n.color = pixie.Color(1, 0, 1, 1)

ctx = image.new_context()
ctx.fill_style = active_p
ctx.fill_rect(margin+poly["width_ext"], margin, mos_tot[0], active["width"])

ctx.fill_style = active_n
ctx.fill_rect(margin+mos["width"]+well["space"], margin+active["width"], mos_tot[0], active["width"])

image.write_file("test.png")
