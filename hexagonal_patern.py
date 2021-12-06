
import math

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


def generaCirclePoints(cpoint, phase_offet, size, x_center, y_center):
    points = []
    phase_delta = 2.0*math.pi/cpoint
    for i in range(cpoint):
        phase = phase_offet + phase_delta*i

        y = math.sin(phase) * size/2 + y_center
        x = math.cos(phase) * size/2 + x_center

        points.append({"x": x, "y": y})

    return points

def generateHexagonPoints(size, position, phase, limit):
    points = []

    x_delta = position["x"];
    y_delta = position["y"];

    point_count = 6
    points = generaCirclePoints(point_count, phase, size, x_delta, y_delta)

    violated_count = 0
    points_w_md = []
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

def GenerateKerfEstimationPattern(max, min, limit, smpl_spcing, rows):
    xspace = limit["x.max"] - limit["x.min"]
    yspace = limit["y.max"] - limit["y.min"]

    per_row_samples = math.floor(xspace/smpl_spcing)
    rl_spacing = xspace/per_row_samples

    total_sample_count = per_row_samples*rows
    per_sample_delta = -(max-min)/total_sample_count


    per_row_space = yspace/rows

    padding = 5

    paths = []
    print(f"kerf delta is {per_sample_delta}")

    for row in range(rows):
        ystart = padding + per_row_space*row + limit["y.min"]
        yend = ystart + per_row_space - padding
        for sample in range(per_row_samples):
            kerf_distance = max + sample*per_sample_delta + row*per_row_samples*per_sample_delta
            first_line_x = sample*rl_spacing + limit["x.min"]
            second_line_x = first_line_x + kerf_distance

            path_value = "<path\n"
            path_value = path_value + "style=\"fill:none;stroke:#000000;stroke-width:0.033mm;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1\"\n"
            path_value = path_value + f"d=\"M {first_line_x} {ystart} L {first_line_x} {yend} M {second_line_x} {ystart} L {second_line_x} {yend}\" />\n"

            paths.append(path_value)

    return "".join(paths)

def path_svg(path_decription):
    path_value = "<path\n"
    path_value = path_value + "style=\"fill:none;stroke:#000000;stroke-width:0.033mm;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1\"\n"
    path_value = path_value + "d=\"" + path_decription + "\" />\n"

    return path_value

def draw_paths(delta, pattern_limit, params):

    # configurable
    phase = delta
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


    conf_num = 105
    x_size = conf_num
    y_size = x_size
    x_correction = -(conf_num/2 +1)
    y_correction = x_correction

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


def generate_hexagonal_patern_paths(parameters):
    x_limit = parameters["x_limit"]
    y_limit = parameters["y_limit"]
    padding_procent = parameters["padding_procent"]


    padding = x_limit*padding_procent
    y_padding_procent = 0.9 
    y_padding = padding*y_padding_procent

    x_beatwean_section_space = parameters["secion_padding"]
    y_beatwean_section_space = x_beatwean_section_space * y_padding_procent

    x_section_count = parameters["x_section_count"]
    y_section_count = parameters["y_section_count"]

    hsize = []
    hspacing = []

    if parameters["predefined_size_and_spacing"] == False:

        start_hexagon_size = parameters["start_hexagon_size"]
        end_hexagon_size = parameters["end_hexagon_size"]
        start_hexagon_spacing = parameters["start_hexagon_spacing"]
        end_hexagon_spacing = parameters["end_hexagon_spacing"]

        hexagon_size_delta = -(start_hexagon_size - end_hexagon_size)/y_section_count
        hexagon_spacing_delta = -(start_hexagon_spacing - end_hexagon_spacing)/x_section_count


        for y_section in range(y_section_count):
            hsize.append([])
            hspacing.append([])
            for x_section in range(x_section_count):
                hsize[y_section].append(start_hexagon_size + y_section*hexagon_size_delta)
                hspacing[y_section].append(start_hexagon_spacing + x_section*hexagon_spacing_delta)

    else:
        if len(parameters["size_array"]) != y_section_count and all(len(row) == x_section_count for row in parameters["size_array"]) :
            raise "nie zgadza sie size_array"
        else:
            hsize = parameters["size_array"]

        if len(parameters["spacing_array"]) != y_section_count and all(len(row) == x_section_count for row in parameters["spacing_array"]) :
            raise "nie zgadza sie spacing_array"
        else:
            hspacing = parameters["spacing_array"]



    x_space_wout_padding = (x_limit - 2*padding)
    y_space_wout_padding = (y_limit - 2*y_padding)

    x_section_space = x_space_wout_padding - (x_section_count-1)*x_beatwean_section_space
    y_section_space = y_space_wout_padding - (y_section_count-1)*y_beatwean_section_space

    x_section_width = x_section_space/x_section_count
    y_section_height = y_section_space/y_section_count
    print(y_section_space, y_limit, y_padding, y_beatwean_section_space, y_section_height)

    xa = parameters["x_start"]
    xb = xa + x_limit

    ya = parameters["y_start"]
    yb = ya + y_limit

    x1 = parameters["x_start"] + padding
    x2 = x1 + x_space_wout_padding
    y1 = parameters["y_start"] + y_padding
    y2 = y1 + y_space_wout_padding

    all_paths = []



    kerf_sections = 0
    kerf_limit = {
                "x.min": x1, "x.max": x2,
                "y.min": y1, "y.max": y1 + kerf_sections*y_section_height + (kerf_sections-1)*y_beatwean_section_space
            } 

    if parameters["add_holes"]:
        x_center = xa + parameters["hole_offest"]
        y_center = ya + parameters["hole_offest"]
        
        cpoints = generaCirclePoints(20, 0, parameters["hole_size"], x_center, y_center)
        cpoints_w_md = []
        for cpoint in cpoints:
            cpoints_w_md.append({"point": cpoint})
        svg_path = path_svg(generatePathDescription(cpoints_w_md))
        all_paths.append(svg_path)

        x_center = xb - parameters["hole_offest"]
        y_center = ya + parameters["hole_offest"]
        
        cpoints = generaCirclePoints(20, 0, parameters["hole_size"], x_center, y_center)
        cpoints_w_md = []
        for cpoint in cpoints:
            cpoints_w_md.append({"point": cpoint})
        svg_path = path_svg(generatePathDescription(cpoints_w_md))
        all_paths.append(svg_path)

        x_center = xb - parameters["hole_offest"]
        y_center = yb - parameters["hole_offest"]
        
        cpoints = generaCirclePoints(20, 0, parameters["hole_size"], x_center, y_center)
        cpoints_w_md = []
        for cpoint in cpoints:
            cpoints_w_md.append({"point": cpoint})
        svg_path = path_svg(generatePathDescription(cpoints_w_md))
        all_paths.append(svg_path)

        x_center = xa + parameters["hole_offest"]
        y_center = yb - parameters["hole_offest"]
        
        cpoints = generaCirclePoints(20, 0, parameters["hole_size"], x_center, y_center)
        cpoints_w_md = []
        for cpoint in cpoints:
            cpoints_w_md.append({"point": cpoint})
        svg_path = path_svg(generatePathDescription(cpoints_w_md))
        all_paths.append(svg_path)


    if parameters["add_holes"]:
        cpoints = [
            {"x": xa + parameters["border_offset"], "y": ya + parameters["border_offset"]},
            {"x": xa + parameters["border_offset"], "y": yb - parameters["border_offset"]},
            {"x": xb - parameters["border_offset"], "y": yb - parameters["border_offset"]},
            {"x": xb - parameters["border_offset"], "y": ya + parameters["border_offset"]}
        ]
        cpoints_w_md = []
        for cpoint in cpoints:
            cpoints_w_md.append({"point": cpoint})
        svg_path = path_svg(generatePathDescription(cpoints_w_md))
        all_paths.append(svg_path)

    # kerf_paths = GenerateKerfEstimationPattern(3.0, 0.06, kerf_limit, 5.0, 4)
    # all_paths.append(kerf_paths)
    shrinkage_factor = parameters["shrinkage_factor"]

    for x_section in range(x_section_count):
        for y_section in range(y_section_count):
            if(y_section < kerf_sections):
                continue

            x_min = x1 + (x_section_width+x_beatwean_section_space)*x_section
            x_center = x_min + x_section_width/2.0
            x_max = x_min + x_section_width

            y_min = y1 + (y_section_height+y_beatwean_section_space)*y_section
            y_center = y_min + y_section_height/2.0
            y_max = y_min + y_section_height

            section_limit = {
                "x.min": x_min, "x.max": x_max - y_section*shrinkage_factor*0.7,
                "y.min": y_min, "y.max": y_max - y_section*shrinkage_factor
            } 

            print(section_limit, y_section_space)  
            hexagon_size = hsize[y_section][x_section]
            hexagon_spacing = hspacing[y_section][x_section]
            params = [hexagon_size, hexagon_spacing]
            
            section_paths = draw_paths(math.pi*2 * 1.2, section_limit,params)
            all_paths.append(section_paths)

    return all_paths
