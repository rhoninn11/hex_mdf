import math
import time 

def fit_points_to_the_limit(points, points_in_range, limit):

    return points_in_range

def generateHexagon(size, position, phase, limit):
    d = []
    points = []

    x_delta = position["x"];
    y_delta = position["y"];

    point_count = 6
    phase_delta = 2.0*math.pi/point_count
    phase_offet = phase
    for i in range(point_count):
        phase = phase_offet + phase_delta*i;

        y = math.sin(phase) * size/2 + y_delta;
        x = math.cos(phase) * size/2 + x_delta;

        points.append({"x": x, "y": y})

    points_in_range = []
    for point in points:
        xmaxcond = point["x"] > limit["x.max"]
        xmincond = point["x"] < limit["x.min"]
        ymaxcond = point["y"] > limit["y.max"]
        ymincond = point["y"] < limit["y.min"]
        if xmaxcond or xmincond or ymaxcond or ymincond:
            points_in_range.append(None)
        else:
            points_in_range.append(point)

    limited_point = fit_points_to_the_limit(points, points_in_range, limit)
    
    for point in limited_point:
        if point is None:
            continue;

        if(len(d) == 0):
            d.append(f'M {point["x"]} {point["y"]} ')
        else:
            d.append(f'L {point["x"]} {point["y"]} ')

    d.append("Z")
    return "".join(d)


y = 4

parzysty_x = 0;
nieparzysty_x = 2;


header = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!-- Created with Inkscape (http://www.inkscape.org/) -->

<svg
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:cc="http://creativecommons.org/ns#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   width="210mm"
   height="297mm"
   viewBox="0 0 210 297"
   version="1.1"
   id="svg8"
   inkscape:export-filename="/home/leszek/Pulpit/elo.svg.png"
   inkscape:export-xdpi="299"
   inkscape:export-ydpi="299"
   inkscape:version="0.92.5 (2060ec1f9f, 2020-04-08)"
   sodipodi:docname="rysunek.svg">
  <g
     inkscape:label="Layer 1"
     inkscape:groupmode="layer"
     id="layer1">'''
tail = '''</g>
</svg>'''
    # <path
    #    style="fill:none;stroke:#000000;stroke-width:0.26458332mm;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1"
    #    d="m 9.6383926,12.761904 -0.9449403,7.748512 3.9687497,4.157738 7.370536,-2.078869 1.133928,-8.504464 -3.212797,-4.7247023 z"/>


def draw_paths(delta, pattern_limit):

    # configurable
    phase = delta;
    hexagon_size = 3
    hexagon_spacing = 4
    # configurable

    mid_triangle_space = math.pi /6
    spacing_factor = math.cos(mid_triangle_space)
    hexagon_spacing_real = spacing_factor*hexagon_spacing


    phase_for_delta_1 = phase + mid_triangle_space
    phase_for_delta_2 = phase - mid_triangle_space
    x_delta_1 = math.cos(phase_for_delta_1) * hexagon_spacing_real
    y_delta_1 = math.sin(phase_for_delta_1) * hexagon_spacing_real
    x_delta_2 = math.cos(phase_for_delta_2) * hexagon_spacing_real
    y_delta_2 = math.sin(phase_for_delta_2) * hexagon_spacing_real


    conf_num = 177;
    x_size = conf_num;
    y_size = x_size
    x_correction = -(conf_num/2 +1);
    y_correction = x_correction;

    hexagon_center = {"x": 110, "y": 150}

    paths = []

    for y in range(y_size):
        y_index = y + y_correction

        for x in range(x_size):
            
            x_index = x + x_correction

            x_offset = x_delta_1*x_index + x_delta_2*y_index
            y_offset = y_delta_1*x_index + y_delta_2*y_index
            hex_position = {"x": hexagon_center["x"] +  x_offset, "y": hexagon_center["y"] + y_offset}


            d_value = generateHexagon(hexagon_size, hex_position, phase, pattern_limit )
            if len(d_value) == 0 or len(d_value) == 1:
                continue

            path_value = "<path\n"
            path_value = path_value + "style=\"fill:none;stroke:#000000;stroke-width:0.1mm;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1\"\n"
            path_value = path_value + "d=\"" + d_value + "\" />\n"

            paths.append(path_value)

    return "".join(paths)


animation_points = 1;

x_limit = 210.0
y_limit = 297.0
padding_procent = 0.02


padding = x_limit*padding_procent
y_padding_procent = 0.9 
y_padding = padding*y_padding_procent


x_beatwean_section_space = 3
y_beatwean_section_space = x_beatwean_section_space * y_padding_procent

x_section_count = 3
y_section_count = 4

x_section_space = (x_limit - 2*padding) - (x_section_count-1)*x_beatwean_section_space;
y_section_space = (y_limit - 2*y_padding) - (y_section_count-1)*y_beatwean_section_space;

x_section_width = x_section_space/x_section_count;
y_section_height = y_section_space/y_section_count;
print(y_section_space, y_limit, y_padding, y_beatwean_section_space, y_section_height)

x1 = padding
x2 = x_limit - padding
y1 = y_padding
y2 = y_limit - y_padding

all_paths = []

for x_section in range(x_section_count):
    for y_section in range(y_section_count):

        x_min = x1 + (x_section_width+x_beatwean_section_space)*x_section
        x_center = x_min + x_section_width/2.0
        x_max = x_min + x_section_width

        y_min = y1 + (y_section_height+y_beatwean_section_space)*y_section
        y_center = y_min + y_section_height/2.0
        y_max = y_min + y_section_height

        section_limit = {
            "x.min": x_min, "x.max": x_max,
            "y.min": y_min, "y.max": y_max
        } 

        print(section_limit, y_section_space)  
        
        section_paths = draw_paths(math.pi*2 * 1.2, section_limit);
        all_paths.append(section_paths)

svg = []
svg.append(header);
svg.append("".join(all_paths))
svg.append(tail);

result_svg = "".join(svg);

with open('result.svg', 'w') as file:
    file.write(result_svg)
