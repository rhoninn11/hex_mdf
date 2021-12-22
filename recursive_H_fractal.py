

from util import points_2_path

DR = { 
    'N': "N",
    "E": "E",
    "S": "S",
    "W": "W"
}
DR_NUM = {
    "N": {"x": 0, "y": 1},
    "E": {"x": 1, "y": 0},
    "S": {"x": 0, "y": -1},
    "W": {"x": -1, "y": 0},
}

CHILD_DR = {
    "N": ["E", "W"],
    "E": ["S", "N"],
    "S": ["W", "E"],
    "W": ["N", "S"],
}
R = 0
L = 1

X = "x"
x = "x"
Y = "y"
y = "y"



def fractal_gen(origin, length, levels, direction):
    paths = []
    if levels == 0:
        return paths

    points = []
    factor = 1
    for i in range(levels+1):
        factor = factor*0.7071067
    thisckenss = length*factor
    childs = CHILD_DR[direction]
    
    first = True
    my_origin = 0

    for child in childs:
        last_child = child
        
        point = {X:origin[X], Y:origin[Y]}
        # add thickness
        # point["x"] = origin["x"] + DR_NUM[child]["x"]*length/2
        # point["y"] = origin["y"] + DR_NUM[child]["y"]*length/2

        # middle_point = point
        a_point = origin.copy()
        b_point = origin.copy()

        thic_dir = CHILD_DR[child][R]
        thic_delta = DR_NUM[thic_dir]
        child_delta = DR_NUM[child]
        # add thickness
        a_point[X] = origin[X] + thic_delta[X]*thisckenss/2
        a_point[Y] = origin[Y] + thic_delta[Y]*thisckenss/2

        # move in child direction
        b_point[X] = a_point[X] + child_delta[X]*length/2
        b_point[Y] = a_point[Y] + child_delta[Y]*length/2
        points.append(a_point)
        points.append(b_point)

        child_origin = origin.copy()
        # remove thickness / generate child origin 
        child_origin[X] = b_point[X] - thic_delta[X]*thisckenss/2
        child_origin[Y] = b_point[Y] - thic_delta[Y]*thisckenss/2
        
        # gen child points
        fractal_points = fractal_gen(child_origin, length*0.7071067, levels-1, child)
        points.extend(fractal_points)

        # nie ważne
        a_point = origin.copy()
        b_point = origin.copy()

        thic_dir = CHILD_DR[child][L]
        thic_delta = DR_NUM[thic_dir]
        child_delta = DR_NUM[child]
        # add thickness
        a_point[X] = origin[X] + thic_delta[X]*thisckenss/2
        a_point[Y] = origin[Y] + thic_delta[Y]*thisckenss/2

        # move in child direction
        b_point[X] = a_point[X] + child_delta[X]*length/2
        b_point[Y] = a_point[Y] + child_delta[Y]*length/2


        points.append(b_point)
        points.append(a_point)

    return points

    
        

    
