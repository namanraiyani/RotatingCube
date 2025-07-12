import os 
import math 
import numpy as np
import time
def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def rotate(x, y, z, ax, ay, az):
    ax, ay, ax = math.radians(ax), math.radians(ay), math.radians(az)
    rotation_matrix = [
        [math.cos(ay) * math.cos(az), math.cos(az) * math.sin(ax) * math.sin(ay) - math.cos(ax) * math.sin(az), math.sin(ax) * math.sin(az) + math.cos(ax) * math.cos(az) * math.sin(ay)],
        [math.cos(ay) * math.sin(az), math.cos(ax) * math.cos(az) + math.sin(ax) * math.sin(ay) * math.sin(az), math.cos(ax) * math.sin(ay) * math.sin(az) - math.cos(az) * math.sin(ax)],
        [-math.sin(ay),               math.cos(ay) * math.sin(ax),                                                math.cos(ax) * math.cos(ay)]
    ]

    return [round(coord, 12) for coord in np.dot(rotation_matrix, [x, y, z])]

def project(x, y, z, width, height, scale = 200, distance = 5):
    return [int(((width/2) + (x*scale) / (z+distance))), int((height/2) - (y*scale / (z+distance)))]

vertices = [
    [1, 1, 1],
    [1, 1, -1],
    [-1, 1, -1],
    [-1, 1, 1],
    [1, -1, 1],
    [1, -1, -1],
    [-1, -1, -1],
    [-1, -1, 1]
]

edges = [
    (0,1), (1,2), (2,3), (3,0),
    (4,5), (5,6), (6,7), (7,4),
    (0,4), (1,5), (2,6), (3,7)
]
clear()
width = 625
height = 130

def draw_points(screen):
    projected = []
    for x, y, z in vertices:
        x,y = project(x,y,z,width,height)
        projected.append((x,y))
    return screen, projected
    
def draw_edges(screen, edges, projected):
    for e1,e2 in edges:
        x1, y1 = projected[e1]
        x2, y2 = projected[e2]
        dx = x2 - x1
        dy = y2 - y1
        steps = max(abs(dx), abs(dy))
        for i in range(steps):
            xi = int(x1 + dx*i/steps)
            yi = int(y1 + dy*i/steps)
            if 0<=xi<width and 0<=yi<height:
                screen[yi][xi] = '*'
    return screen

while True:
    clear()
    screen = [[' ']*width for _ in range(height)]
    screen, projected = draw_points(screen)
    screen = draw_edges(screen, edges, projected)
    for row in screen:
        print(''.join(row))
    for i in range(len(vertices)):
        vertices[i] = rotate(vertices[i][0], vertices[i][1], vertices[i][2], 1, 0.7, 0.007)
    time.sleep(0.0075)
