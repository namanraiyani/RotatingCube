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
    ax, ay, az = math.radians(ax), math.radians(ay), math.radians(az)
    rotation_matrix = [
        [math.cos(ay) * math.cos(az), math.cos(az) * math.sin(ax) * math.sin(ay) - math.cos(ax) * math.sin(az), math.sin(ax) * math.sin(az) + math.cos(ax) * math.cos(az) * math.sin(ay)],
        [math.cos(ay) * math.sin(az), math.cos(ax) * math.cos(az) + math.sin(ax) * math.sin(ay) * math.sin(az), math.cos(ax) * math.sin(ay) * math.sin(az) - math.cos(az) * math.sin(ax)],
        [-math.sin(ay),               math.cos(ay) * math.sin(ax),                                                math.cos(ax) * math.cos(ay)]
    ]

    return [round(coord, 12) for coord in np.dot(rotation_matrix, [x, y, z])]

def project(x, y, z, width, height, scale = 200, distance = 5):
    aspect_ratio=2
    return [int(((width/2) + (x*scale*aspect_ratio) / (z+distance))), int((height/2) - (y*scale / (z+distance)))]

def inside_quad(px,py,x1,y1,x2,y2,x3,y3,x4,y4):
    def edge_test(xa,ya,xb,yb):
        return (px-xa)*(yb-ya)-(py-ya)*(xb-xa)
    d1 = edge_test(x1,y1,x2,y2)
    d2 = edge_test(x2,y2,x3,y3)
    d3 = edge_test(x3,y3,x4,y4)
    d4 = edge_test(x4,y4,x1,y1)
    has_neg = (d1<0) or (d2<0) or (d3<0) or (d4<0)
    has_pos = (d1>0) or (d2>0) or (d3>0) or (d4>0)
    return not (has_neg and has_pos)

def get_depth(face):
    return sum(vertices[i][2] for i in face) / len(face)

def fill_face(screen, projected, zbuffer):
    sorted_faces = sorted(faces, key = get_depth, reverse=True)
    for face in sorted_faces:
        x1, y1=projected[face[0]]
        x2, y2=projected[face[1]]
        x3, y3=projected[face[2]]
        x4, y4=projected[face[3]]

        z1,z2,z3,z4 = vertices[face[0]][2],vertices[face[1]][2],vertices[face[2]][2],vertices[face[3]][2]

        x_min = max(min(x1,x2,x3,x4),0)
        x_max = min(max(x1,x2,x3,x4),width-1)
        y_min = max(min(y1,y2,y3,y4),0)
        y_max = min(max(y1,y2,y3,y4),height-1)
        n = get_normal(vertices[face[0]], vertices[face[1]], vertices[face[2]])
        if np.dot(n, view_direction) < 0:
            continue
        char = get_ascii(get_intensity(n,light_vector))
        for i in range(x_min, x_max+1):
            for j in range(y_min, y_max+1):
                if(inside_quad(i,j,x1,y1,x2,y2,x3,y3,x4,y4)):
                    z = (z1+z2+z3+z4) / 4
                    if z < zbuffer[j][i]:
                        zbuffer[j][i] = z
                        screen[j][i] = char
                    # screen[j][i]='█'
                    # screen[j][i] = char
                    # screen[j][i]='▒'
    return screen

def get_normal(v1,v2,v3):
    x1,y1,z1,x2,y2,z2,x3,y3,z3 = v1[0],v1[1],v1[2], v2[0],v2[1],v2[2],v3[0],v3[1],v3[2]
    v1x, v1y, v1z = x2-x1, y2-y1, z2-z1
    v2x, v2y, v2z = x3-x1, y3-y1, z3-z1
    n = np.array([v1y*v2z - v1z*v2y, -v1x*v2z + v1z*v2x, v1x*v2y - v1y*v2x])
    return n / np.linalg.norm(n)

def get_intensity(n, light_vector):
    return max(0, np.dot(n, light_vector))

def get_ascii(intensity):
    shades = ['.', ':', '-', '=', '+', '*', '#', '%', '@', '█']
    ind = int(intensity * len(shades)-1)
    # print(ind)
    return shades[ind]


view_direction = [0,0,1]
light_vector = [-1,-1,-1]
light_vector = light_vector / np.linalg.norm(light_vector)

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

faces = [
    [0,1,2,3],
    [5,1,0,4],
    [7,4,5,6],
    [3,7,4,0],
    [2,6,7,3],
    [5,6,2,1]
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
        # screen[y][x] = '*'
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
                screen[yi][xi] = '█'
    return screen

def main():
    while True:
        clear()
        screen = [[' ']*width for _ in range(height)]
        screen, projected = draw_points(screen)
        zbuffer = [[float('inf')]*width for _ in range(height)]
        screen = fill_face(screen,projected,zbuffer)
        screen = draw_edges(screen, edges, projected)

        for row in screen:
            print(''.join(row))

        for i in range(len(vertices)):
            vertices[i] = rotate(vertices[i][0], vertices[i][1], vertices[i][2], 0.3, 0.7, 0.5)
        time.sleep(1/30)

if __name__ == "__main__":
    main()
