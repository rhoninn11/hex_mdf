

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

def fractal_gen(origin, length, levels, direction):
    paths = []
    if levels == 0:
        return paths

    points = []
    childs = CHILD_DR[direction]
    for child in childs:
        point = {"x":0, "y":0}
        point["x"] = origin["x"] + DR_NUM[child]["x"]*length/2
        point["y"] = origin["y"] + DR_NUM[child]["y"]*length/2

        points.append(point)
        paths.extend(fractal_gen(point, length*0.7071067, levels-1, child))

    paths.append(points_2_path(points))
    return paths

    
        

    
