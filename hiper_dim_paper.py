import math
from pickle import FALSE

def trace_circle(circ_dim):
    result = []

    init_phase = math.pi/2
    finish_phase = 5*math.pi/2


    phase_delta = 2*math.pi/circ_dim;
    phase = init_phase
    while phase < finish_phase:
        polarity = math.sin(phase)
        side = math.cos(phase)
        result.append([polarity, side])
        phase = phase + phase_delta

    return result;
    
# transmultification
def transmult(data, tanslat, mult):
    r = []
    xy = [0,1]
    for point in data:
        r1 = []
        for dir in xy:
            r2 = mult*point[dir] + tanslat[dir]
            r1.append(r2)
        r.append(r1)
    
    return r;

def gon_points_gen(gon_dim, origin, size):
    r = trace_circle(gon_dim)
    r1 = transmult(r, origin, size);
    # if tylko: trace_circle(gon_dim).transmult(origin, size) było możliwe
    return r1;

def gen_hex_points(origin, size):
    gon_points = gon_points_gen(6, origin, size);
    return gon_points

factor = 0.99
delta = 0.02
verts = 6
middle_root = [0.0,0.0]

def gen_hex_grid(origin, size, asize):
    
    outter_roots = trace_circle(6);
    outter_roots  = transmult(outter_roots, origin, size);
    inner_root = transmult([middle_root], origin, size)[0];
    roots = [inner_root]
    roots.extend(outter_roots)
    grid = []
    for root_to_grid in roots:
        root_grid = gen_hex_points(root_to_grid, size/2 - asize*delta)
        grid.append(root_grid)

    return grid;

def gen_hex_grid2(origin, size, asize):
    
    outter_roots = trace_circle(6);
    outter_roots  = transmult(outter_roots, origin, size);
    inner_root = transmult([middle_root], origin, size)[0];
    roots = [inner_root]
    roots.extend(outter_roots)
    
    grid = []
    for root_to_grid in roots:
        root_grid = gen_hex_grid(root_to_grid, size/3 - asize*delta/2, size)
        grid.append(root_grid)
        root_grid = gen_hex_points(root_to_grid, size/2 - asize*delta/3)
        grid.append(root_grid)

    return grid;
    
def gen_hex_grid3(origin, size, asize):
    
    outter_roots = trace_circle(6);
    outter_roots  = transmult(outter_roots, origin, size);
    inner_root = transmult([middle_root], origin, size)[0];
    roots = [inner_root]
    roots.extend(outter_roots)
    
    grid = []
    for root_to_grid in roots:
        root_grid = gen_hex_grid2(root_to_grid, size/3 - asize*delta/2, size)
        grid.append(root_grid)
        root_grid = gen_hex_points(root_to_grid, size/2 - asize*delta/3)
        grid.append(root_grid)

    return grid;

def gen_hex_full_page_grid(origin, size, asize):
    inner_root = transmult([middle_root], origin, size)[0];
    dirs = trace_circle(6)
    retrans_dirs = transmult(dirs, middle_root, size)

    layers_count = 36
    ifix = [min(i%6,1)*i for i in range((layers_count-1)*6 + 1)]
    root_layers = [[inner_root]]

    for l in range(layers_count):
        layer = []

        for i in range(6):
            idx = [ifix[i*l + n] for n in range(l+1) ]
            root_to_retrans = [ root_layers[l][ifix[i*l + n]] for n in range(l+1) ]
            retrans_root = transmult(root_to_retrans, retrans_dirs[i], 1)
            layer.extend(retrans_root)

        ifix[l*6] = l*6 
        root_layers.append(layer)

    r = []
    for l in root_layers:
        r.extend(l)
    
    grid = []
    for loc in r:
        root_grid = gen_hex_points(loc, size/2 - asize*delta/3)
        grid.append(root_grid)

    return grid




def gen_hex_full_page_grid2(origin, size, asize):
    
    outter_roots = trace_circle(6);
    outter_roots  = transmult(outter_roots, origin, size);
    inner_root = transmult([middle_root], origin, size)[0];
    
    outerrer_roots = []
    dirs = trace_circle(6)
    retrans_dirs = transmult(dirs, middle_root, size)
    ifix = [ i%6 for i in range(7)]
    for i in range(6):
        root_to_retrans = [outter_roots[i], outter_roots[ifix[i+1]]]
        retrans_root = transmult(root_to_retrans, retrans_dirs[i], 1)
        outerrer_roots.extend(retrans_root)

    ifix = [ i for i in range(13) ]
    ifix[12] = 0;
    outerrerer_roots = []
    for i in range(6):
        root_to_retrans = [outerrer_roots[i*2], outerrer_roots[ifix[i*2 + 1]], outerrer_roots[ifix[i*2 + 2]]]
        retrans_root = transmult(root_to_retrans, retrans_dirs[i], 1)
        outerrerer_roots.extend(retrans_root)
        
    roots = [inner_root]
    roots.extend(outter_roots)
    roots.extend(outerrer_roots)
    roots.extend(outerrerer_roots)

    grid = []
    for root_to_grid in roots:
        root_grid = gen_hex_grid2(root_to_grid, size/3 - asize*delta/2, size)
        grid.append(root_grid)
        root_grid = gen_hex_points(root_to_grid, size/2 - asize*delta/3)
        grid.append(root_grid)

    return grid;


def isParseLevel(data_list):
    list_probe_top = data_list
    isNotEmptyList_top = isinstance(list_probe_top, list)
    list_probe_inner = data_list[0] 
    isNotEmptyList_inner = isinstance(list_probe_inner, list)

    goDeaper = False
    if isNotEmptyList_top and isNotEmptyList_inner:
        isInnerListIsNumerical = not isinstance(list_probe_inner[0], list)
        # lista wewnętrzna jest listą współżędnych, lista zewnętrzn jest grupą
        goDeaper = isInnerListIsNumerical

    return not goDeaper

def flat(data_list):
    r = []

    if isParseLevel(data_list):
        for branch in data_list:
            r1 = flat(branch)
            r.extend(r1)
        return r

    point_list = data_list
    for cord_list in point_list:
        r.append(cord2point(cord_list))

    return [r]
    

def cord2point(cords):
    return {"x": cords[1], "y": cords[0]}

def paper_pattern_gen():

    origin = [148,210]
    size = 3

    hexagon_points = gen_hex_full_page_grid(origin, size, size)
    r = flat(hexagon_points)
    return r