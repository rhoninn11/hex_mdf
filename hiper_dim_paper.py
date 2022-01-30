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
delta = 0.05
verts = 6
middle_root = [0.0,0.0]

def trace_hex(phase_shift = False):
    if(phase_shift):
        trace_pre = trace_circle(12)
        trace_post = []
        for i in range(len(trace_pre)):
            if i%2 == 1:
                trace_post.append(trace_pre[i])

        return trace_post
    else:
        return trace_circle(6)


def gen_hex_roots(origin, size, phase_shift = False):
    outter_roots = trace_hex(phase_shift)
    outter_roots  = transmult(outter_roots, origin, size);
    inner_root = transmult([middle_root], origin, size)[0];
    roots = [inner_root]
    roots.extend(outter_roots)

    return roots


def gen_hex_grid(origin, size, asize, phase_shift = False):
    grid = []
    roots = gen_hex_roots(origin,size,phase_shift)
    for root_to_grid in roots:
        root_grid = gen_hex_points(root_to_grid, size/2 - asize*delta)
        grid.append(root_grid)

    return grid;

def gen_hex_grid2(origin, size, asize, phase_shift = False):
    
    grid = []
    roots = gen_hex_roots(origin,size,phase_shift)
    for root_to_grid in roots:
        root_grid = gen_hex_grid(root_to_grid, size/3 - asize*delta/2, size, phase_shift)
        grid.append(root_grid)
        root_grid = gen_hex_points(root_to_grid, size/2 - asize*delta/3)
        grid.append(root_grid)

    return grid;
    
def gen_hex_grid3(origin, size, asize, phase_shift = False):
    grid = []
    roots = gen_hex_roots(origin,size,phase_shift)
    for root_to_grid in roots:
        root_grid = gen_hex_grid2(root_to_grid, size/3 - asize*delta/2, size, phase_shift)
        grid.append(root_grid)
        root_grid = gen_hex_points(root_to_grid, size/2 - asize*delta/3)
        grid.append(root_grid)

    return grid;

def displocation(a0, a1):
    return [a1[0] - a0[0], a1[1] - a0[1]]

def norm(a0):
    len_sq = a0[0]*a0[0] + a0[1]*a0[1]
    return math.sqrt(len_sq)

def normalize(a0):
    len = norm(a0)
    return [a0[0]/len, a0[1]/len]

def hex_sum(a0, a1, delta):

    disloc = displocation(a0, a1)
    dir = normalize(disloc);
    dir_otho = [dir[1], -dir[0]]
    length = norm(disloc)
    
    middle = [a0[0] + dir[0]*length/2, a0[1] + dir[1]*length/2]
    rndr_length = length-2*delta

    rndr_dir = [dir[0]*rndr_length/2, dir[1]*rndr_length/2]
    start = [middle[0] + rndr_dir[0], middle[1] + rndr_dir[1]]
    end = [middle[0] - rndr_dir[0], middle[1] - rndr_dir[1]]

    rndr_ortho_length = rndr_length*math.sqrt(3)
    rndr_ortho_dir = [dir_otho[0]*rndr_ortho_length/2, dir_otho[1]*rndr_ortho_length/2]
    l1 = [middle[0] + rndr_ortho_dir[0], middle[1] + rndr_ortho_dir[1]]
    l3 = [middle[0] - rndr_ortho_dir[0], middle[1] - rndr_ortho_dir[1]]
    
    return [start, l1, end, l3]


def sum(hex1, hex2, dir):

    hex1_idx = [];
    for i in range(len(hex1)):
        sum = hex1[i][0]*dir(0) + hex1[i][1]*dir(1);
        print(sum, i)
    hex2_idx = [];
    for i in range(len(hex2)):
        sum = hex1[i][0]*dir(0) + hex1[i][1]*dir(1);
        print(sum, i)

    return [hex1[0], hex2[0]]

def gen_hex_grid4(origin, size, asize, phase_shift = False):
    grid = []
    
    roots = gen_hex_roots(origin,size,phase_shift)
    alt_roots = gen_hex_roots(origin,size*math.sqrt(3)/3*2,not phase_shift)
    alt_roots1 = gen_hex_roots(origin,size*math.sqrt(3),not phase_shift)
    delta = 0.5
    for root_to_grid in roots:
        root_grid = gen_hex_points(root_to_grid, size/math.sqrt(3) - delta)
        grid.append(root_grid)

    # for root_to_grid in alt_roots:
    #     root_grid = gen_hex_points(root_to_grid, size/math.sqrt(3) - delta)
    #     grid.append(root_grid)

    # for root_to_grid in alt_roots1:
    #     root_grid = gen_hex_points(root_to_grid, size/math.sqrt(3) - delta)
    #     grid.append(root_grid)

    alt_roots2 = alt_roots[1:7];
    alt_roots3 = alt_roots1[1:7];

    for i in range(len(alt_roots2)):
        dir = [alt_roots2[i], alt_roots3[i]]
        sum = hex_sum(alt_roots2[i], alt_roots3[i], delta)
        grid.append(sum)

    return grid;

def gen_hex_full_page_grid(origin, size, asize, phase_shift = False):
    inner_root = transmult([middle_root], origin, size)[0];
    dirs = trace_hex(phase_shift)
    retrans_dirs = transmult(dirs, middle_root, size)

    base = 1
    layers_count = base*3
    ifix = [min(i%6,1)*i for i in range((layers_count-1)*6 + 1)]

    r = []
    r1 = [inner_root]
    root_layers = [[inner_root]]
    for l in range(layers_count):
        layer = []

        for i in range(6):
            idx = [ifix[i*l + n] for n in range(l+1) ]
            root_to_retrans = [ root_layers[l][idx[n]] for n in range(l+1) ]
            retrans_root = transmult(root_to_retrans, retrans_dirs[i], 1)
            layer.extend(retrans_root)

        ifix[l*6] = l*6 
        if (l+1)%3 == 0:
            print(l)
            for loc in range(len(layer)):
                if loc%3 == 0:
                    r1.append(layer[loc])
                else:
                    r.append(layer[loc])
        else:
            r.extend(layer)
            
        root_layers.append(layer)

    grid1 = []
    for loc in r:
        root_grid = gen_hex_points(loc, size/2-asize*delta*2)
        grid1.append(root_grid)

    grid2 = []
    grid3 = []
    for loc in r1:
        root_grid = gen_hex_points(loc, size/2*3)
        grid2.append(root_grid)
        root_grid1 = gen_hex_points(loc, size/2)
        grid1.append(root_grid1)
        root_grid2 = gen_hex_points(loc, size/4)
        for i in range(3):
            grid3.append([root_grid2[i], root_grid2[i+3]])

    elo = []
    elo.extend(grid1)
    elo.extend(grid2)
    elo.extend(grid3)
    return elo

def gen_hex_full_page_grid2(origin, size, asize, phase_shift = False):
    inner_root = transmult([middle_root], origin, size)[0];
    dirs = trace_hex(phase_shift)
    retrans_dirs = transmult(dirs, middle_root, size)

    base = 1
    layers_count = base*3
    ifix = [min(i%6,1)*i for i in range((layers_count-1)*6 + 1)]

    r = []
    r1 = [inner_root]
    root_layers = [[inner_root]]
    for l in range(layers_count):
        layer = []

        for i in range(6):
            idx = [ifix[i*l + n] for n in range(l+1) ]
            root_to_retrans = [ root_layers[l][idx[n]] for n in range(l+1) ]
            retrans_root = transmult(root_to_retrans, retrans_dirs[i], 1)
            layer.extend(retrans_root)

        ifix[l*6] = l*6 
        if (l+1)%3 == 0:
            print(l)
            for loc in range(len(layer)):
                if loc%3 == 0:
                    r1.append(layer[loc])
                else:
                    r.append(layer[loc])
        else:
            r.extend(layer)
            
        root_layers.append(layer)



    grid = []
    print(math.sqrt(3))
    for loc in r1:
        root_grid = gen_hex_grid4(loc, size, asize, phase_shift)
        grid.append(root_grid)

    return grid

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

    origin = [148,105]
    origin1 = [75,105]
    origin2 = [75,50]
    origin3 = [148,50]
    origin4 = [75,210]
    origin5 = [150,210]
    origin6 = [225,210]
    origin7 = [225,105]
    size = 9

    hexagon_points = gen_hex_full_page_grid(origin, size, size)
    hexagon_points.extend(gen_hex_grid(origin1, size, size))
    hexagon_points.extend(gen_hex_grid2(origin2, size, size))
    hexagon_points.extend(gen_hex_grid3(origin3, size, size))
    hexagon_points.extend(gen_hex_grid(origin4, size, size, True))
    hexagon_points.extend(gen_hex_grid2(origin5, size, size, True))
    hexagon_points.extend(gen_hex_grid3(origin6, size, size, True))
    hexagon_points.extend(gen_hex_full_page_grid2(origin7, size, size, True))
    r = flat(hexagon_points)
    return r