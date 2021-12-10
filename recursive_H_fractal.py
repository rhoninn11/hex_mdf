

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

def fractal_gen(origin, length, levels, direction, term=0):
    paths = []
    if levels == 0:
        return paths

    points = []
    thisckenss = 1
    childs = CHILD_DR[direction]
    
    first = True
    my_origin = 0

    for child in childs:
        last_child = child
        
        point = {"x":origin["x"], "y":origin["y"]}
        # add thickness
        point["x"] = origin["x"] + DR_NUM[child]["x"]*length/2
        point["y"] = origin["y"] + DR_NUM[child]["y"]*length/2
        if first:
            first = False

        fractal_points = fractal_gen(point, length*0.7071067, levels-1, child)
        points.append(point)
        points.extend(fractal_points)

    return points

    
        

    
