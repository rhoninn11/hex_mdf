import math
import time 

def calc_line_params(p1,p2):
    a = (p1["y"] - p2["y"])/(p1["x"] - p2["x"])
    b = p1["y"] - a*p1["x"]
    return {"a": a, "b": b}

def calc_y(line_params, x):
    y = line_params["a"]*x + line_params["b"]
    return y 

def calc_x(line_params, y):
    x = (y - line_params["b"])/line_params["a"]
    return x


def fit_points_to_the_limit(points_w_md, limit):

    point_count = len(points_w_md)

    for i in range(point_count):

        pir = points_w_md[i]["point"]
        pirvc = points_w_md[i]["vc"]

        prev_pir_idx = i-1 if i != 0 else point_count-1
        next_pir_idx = i+1 if i != point_count-1 else 0

        prev_pir = points_w_md[prev_pir_idx]["point"]
        prev_pirvc = points_w_md[prev_pir_idx]["vc"]
        next_pir = points_w_md[next_pir_idx]["point"]
        next_pirvc = points_w_md[next_pir_idx]["vc"]

        pcalc = None
        if pirvc != None:
            if prev_pirvc != None and next_pirvc != None:
                continue

            pcalc = {"x": pir["x"], "y": pir["y"]}
            line_point = {"x": 0, "y": 0}
            if prev_pirvc == None:
                line_point = prev_pir

            if next_pirvc == None:
                line_point = next_pir

            lp = calc_line_params(pcalc, line_point)
            x_target = (limit["x.min"] if  pcalc["x"] < limit["x.min"] else None)
            if x_target != None:
                pcalc["x"] = x_target
                pcalc["y"] = calc_y(lp, pcalc["x"])

            x_target = (limit["x.max"] if  pcalc["x"] > limit["x.max"] else None)
            if x_target != None:
                pcalc["x"] = x_target
                pcalc["y"] = calc_y(lp, pcalc["x"])

            y_target = (limit["y.min"] if  pcalc["y"] < limit["y.min"] else None)
            if y_target != None:
                pcalc["y"] = y_target
                pcalc["x"] = calc_x(lp, pcalc["y"])

            y_target = (limit["y.max"] if  pcalc["y"] > limit["y.max"] else None)
            if y_target != None:
                pcalc["y"] = y_target
                pcalc["x"] = calc_x(lp, pcalc["y"])

        else:
            pcalc = pir

        points_w_md[i]["point"] = pir

    return points_w_md

def sort_points(points_w_md):
    point_count = len(points_w_md)

    sorted_points_w_md = []
    sorted_points_count = 0
    point_index = 0
    started = False
    while sorted_points_count <= point_count - 1:

        next_point_index = point_index + 1 if point_index != point_count - 1 else 0
        point = points_w_md[point_index]
        next_point = points_w_md[next_point_index]

        if point["vc"] == None and next_point["vc"] != None:
            started = True

        if started:
            sorted_points_w_md.append(point)
            sorted_points_count = sorted_points_count + 1

        point_index = next_point_index
    
    return sorted_points_w_md

def calc_squared_distacne(a,b):
    x = a["x"]-b["x"]
    y = a["y"]-b["y"]

    return x*x + y*y

def calc_point_on_line_for_specified_limit(line_prameters, all_limits, specified_limit):
    tmp_point = {}
    if specified_limit == "x.min" or specified_limit == "x.max":
        tmp_point["x"] = all_limits[specified_limit]
        tmp_point["y"] = calc_y(line_prameters, all_limits[specified_limit])
    elif specified_limit == "y.min" or specified_limit == "y.max":
        tmp_point["x"] = calc_x(line_prameters, all_limits[specified_limit])
        tmp_point["y"] = all_limits[specified_limit]
    return tmp_point

def calculate_corner_point(limit, side_1, side_2):

    a = None
    b = None
    if side_1 == "x.min" or side_1 == "x.max":
        a = "x"
    elif side_1 == "y.min" or side_1 == "y.max":
        a = "y"

    if side_2 == "x.min" or side_2 == "x.max":
        b = "x"
    elif side_2 == "y.min" or side_2 == "y.max":
        b = "y"

    if a == b:
        raise "tak nie może być"

    point = {a: limit[side_1], b: limit[side_2]}
    return point

def fit_points_to_the_limit_2(points_w_md, limit):

    # find first with violated conditions

    points_to_fix = sort_points(points_w_md)

    outrim_start = None
    outrim_start_lp = None
    outrim_end = None
    outrim_end_lp = None

    fixed_points = []

    point_count = len(points_to_fix)
    for point_index in range(point_count):
        next_point_index = point_index + 1 if point_index != point_count - 1 else 0

        
        pa = points_to_fix[point_index]["point"]
        pb = points_to_fix[next_point_index]["point"]


        violated_conda = points_to_fix[point_index]["vc"]
        violated_condb = points_to_fix[next_point_index]["vc"]

        lp = calc_line_params(pa,pb)

        outrim_is_starting = violated_conda == None and violated_condb != None
        outrim_is_ending = violated_conda != None and violated_condb == None
        inrim = violated_conda == None and violated_condb == None

        if outrim_is_starting:
            outrim_start_lp = lp
            if len(violated_condb) == 1:
                outrim_start = violated_condb[0]
            else:
                min_squared_distance = 10000000000000
                cond = None
                for vcond in violated_condb:
                    tmp_point = calc_point_on_line_for_specified_limit(outrim_start_lp, limit, vcond)
                    sqdist = calc_squared_distacne(pa, tmp_point)
                    if sqdist < min_squared_distance:
                        min_squared_distance = sqdist
                        cond = vcond
                outrim_start = cond

        elif outrim_is_ending:
            outrim_end_lp = lp
            if len(violated_conda) == 1:
                outrim_end = violated_conda[0]
            else:
                min_squared_distance = 10000000000000
                cond = None
                for vcond in violated_conda:
                    tmp_point = calc_point_on_line_for_specified_limit(outrim_end_lp, limit, vcond)
                    sqdist = calc_squared_distacne(pb, tmp_point)
                    if sqdist < min_squared_distance:
                        min_squared_distance = sqdist
                        cond = vcond
                outrim_end = cond



        if inrim or outrim_is_starting:
            fixed_points.append({"point":pa})
        elif outrim_is_ending:
            outrim_start_point =  calc_point_on_line_for_specified_limit(outrim_start_lp, limit, outrim_start)
            outrim_end_point =  calc_point_on_line_for_specified_limit(lp, limit, outrim_end)
            fixed_points.append({"point":outrim_start_point})
            if outrim_start != outrim_end:
                corrner_point = calculate_corner_point(limit, outrim_start, outrim_end)
                fixed_points.append({"point":corrner_point})
            fixed_points.append({"point":outrim_end_point})
            fixed_points.append({"point":pb})

    return fixed_points


def generateHexagonPoints(size, position, phase, limit):
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

    points_w_md = []
    out_of_range = True
    violated_count = 0
    for point in points:
        xmaxcond = point["x"] > limit["x.max"]
        xmincond = point["x"] < limit["x.min"]
        ymaxcond = point["y"] > limit["y.max"]
        ymincond = point["y"] < limit["y.min"]
        md_point = {"point": point}
        if xmaxcond or xmincond or ymaxcond or ymincond:
            vialoate_cond = []
            if xmaxcond:
                vialoate_cond.append("x.max")
            if xmincond:
                vialoate_cond.append("x.min")
            if ymaxcond:
                vialoate_cond.append("y.max")
            if ymincond:
                vialoate_cond.append("y.min")

            # tu by można dodać
            md_point["vc"] = vialoate_cond
            violated_count = violated_count + 1

        else:
            md_point["vc"] = None

        points_w_md.append(md_point)

    if violated_count == 6:
        return None
    elif 0 < violated_count and violated_count < 6:
        fixed_points = fit_points_to_the_limit_2(points_w_md, limit)
        return fixed_points
    else:
        return points_w_md


def generatePathDescription(points_w_md):
    d = []
    for point_w_md in points_w_md:
        point = point_w_md["point"]

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


def draw_paths(delta, pattern_limit, params):

    # configurable
    phase = delta;
    hexagon_size = params[0]
    hexagon_spacing = params[1] + hexagon_size
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


    conf_num = 105;
    x_size = conf_num;
    y_size = x_size
    x_correction = -(conf_num/2 +1);
    y_correction = x_correction;

    x_center = (pattern_limit["x.min"] + pattern_limit["x.max"])/2.0
    y_center = (pattern_limit["y.min"] + pattern_limit["y.max"])/2.0
    hexagon_center = {"x": x_center, "y": y_center}

    paths = []

    for y in range(y_size):
        y_index = y + y_correction

        for x in range(x_size):
            
            x_index = x + x_correction

            x_offset = x_delta_1*x_index + x_delta_2*y_index
            y_offset = y_delta_1*x_index + y_delta_2*y_index
            hex_position = {"x": hexagon_center["x"] +  x_offset, "y": hexagon_center["y"] + y_offset}


            hex_points = generateHexagonPoints(hexagon_size, hex_position, phase, pattern_limit )
            if hex_points == None:
                continue

            path_value = "<path\n"
            path_value = path_value + "style=\"fill:none;stroke:#000000;stroke-width:0.033mm;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1\"\n"
            path_value = path_value + "d=\"" + generatePathDescription(hex_points) + "\" />\n"

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

x_section_count = 8
y_section_count = 16

start_hexagon_size = 3
start_hexagon_spacing = 1

hexagon_size_delta = -0.20
hexagon_spacing_delta = -0.1

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
        hexagon_size = start_hexagon_size + y_section*hexagon_size_delta
        hexagon_spacing = start_hexagon_spacing + x_section*hexagon_spacing_delta
        params = [hexagon_size, hexagon_spacing]
        
        section_paths = draw_paths(math.pi*2 * 1.2, section_limit,params);
        all_paths.append(section_paths)

svg = []
svg.append(header);
svg.append("".join(all_paths))
svg.append(tail);

result_svg = "".join(svg);

with open('result.svg', 'w') as file:
    file.write(result_svg)

