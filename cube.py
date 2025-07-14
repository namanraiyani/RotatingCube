import os 
import math 
import numpy as np
import time
import sys

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

def project(x, y, z, width, height, scale = 150, distance = 10):
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

def fill_face(screen, projected):
    sorted_faces = sorted(faces, key = get_depth, reverse=True)
    for face in sorted_faces:
        x1, y1=projected[face[0]]
        x2, y2=projected[face[1]]
        x3, y3=projected[face[2]]
        x4, y4=projected[face[3]]
        x_min = max(min(x1,x2,x3,x4),0)
        x_max = min(max(x1,x2,x3,x4),width-1)
        y_min = max(min(y1,y2,y3,y4),0)
        y_max = min(max(y1,y2,y3,y4),height-1)
        n = get_normal(vertices[face[0]], vertices[face[1]], vertices[face[2]])
        center_point = np.mean([vertices[i] for i in face], axis=0)
        light_dir = light_position - center_point
        light_dir /= np.linalg.norm(light_dir)
        if np.dot(n, light_dir) < 0:  
            char = ','
        else:
            char = get_ascii(get_intensity(n, center_point, light_position))
        for i in range(x_min, x_max+1):
            for j in range(y_min, y_max+1):
                if(inside_quad(i,j,x1,y1,x2,y2,x3,y3,x4,y4)):
                    screen[j][i] = char
    return screen

def get_normal(v1,v2,v3):
    x1,y1,z1,x2,y2,z2,x3,y3,z3 = v1[0],v1[1],v1[2], v2[0],v2[1],v2[2],v3[0],v3[1],v3[2]
    v1x, v1y, v1z = x2-x1, y2-y1, z2-z1
    v2x, v2y, v2z = x3-x1, y3-y1, z3-z1
    n = np.array([v1y*v2z - v1z*v2y, -v1x*v2z + v1z*v2x, v1x*v2y - v1y*v2x])
    norm = np.linalg.norm(n)
    if norm == 0:
        return np.array([0, 0, 1])  
    return n / norm

def get_intensity(n, point, light_position):
    light_dir = light_position - point
    distance = np.linalg.norm(light_dir)
    
    if distance == 0:
        return 1.0  

    light_dir /= distance
    angle_factor = np.dot(n, light_dir)
    angle_factor = max(0.0, angle_factor)  
    distance_factor = 1 / (distance ** 1.5)
    intensity = angle_factor * distance_factor * 3
    return min(intensity, 1.0)

def get_ascii(intensity):
    shades = "*0@#"
    ind = int(intensity * (len(shades)-1)) 
    ind = max(0, min(ind, len(shades)-1))
    return shades[ind]

def draw_points(screen):
    projected = []
    for x, y, z in vertices:
        x,y = project(x,y,z,width,height)
        projected.append((x,y))
    return projected
    
def draw_edges(screen, edges, projected):
    for e1,e2 in edges:
        x1, y1 = projected[e1]
        x2, y2 = projected[e2]
        dx = x2 - x1
        dy = y2 - y1
        steps = max(abs(dx), abs(dy))
        for i in range(0,steps,2):
            xi = int(x1 + dx*i/steps)
            yi = int(y1 + dy*i/steps)
            if 0<=xi<width and 0<=yi<height:
                screen[yi][xi] = '.'
    return screen

light_position = np.array([0,1.50,-1.5])

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
    [4,7,6,5],  
    [0,4,5,1],  
    [2,6,7,3],  
    [0,3,7,4], 
    [1,5,6,2]  
]

edges = [
    (0,1), (1,2), (2,3), (3,0),
    (4,5), (5,6), (6,7), (7,4),
    (0,4), (1,5), (2,6), (3,7)
]

width = 225
height = 75

def main():
    clear()
    while True:
        print("\033[H", end='') 
        screen = [[' ']*width for _ in range(height)]
        projected = draw_points(screen)
        screen = draw_edges(screen, edges, projected) 
        screen = fill_face(screen,projected) 
        output = '\n'.join(''.join(row) for row in screen)
        sys.stdout.write(output)
        sys.stdout.flush()

        for i in range(len(vertices)):
            vertices[i] = rotate(vertices[i][0], vertices[i][1], vertices[i][2], 3,2.5,1)

        time.sleep(1/50)

if __name__ == "__main__":
    main()
