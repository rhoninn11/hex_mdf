
# all in svg context
def points_2_D(points):
    d = []
    for point in points:
        if(len(d) == 0):
            d.append(f'M {point["x"]} {point["y"]} ')
        else:
            d.append(f'L {point["x"]} {point["y"]} ')

    d.append("Z")
    return "".join(d)

def points_2_path(points):
    path_value = "<path\n"
    path_value = path_value + "style=\"fill:none;stroke:#000000;stroke-width:0.033mm;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1\"\n"
    path_value = path_value + "d=\"" + points_2_D(points) + "\" />\n"

    return path_value

