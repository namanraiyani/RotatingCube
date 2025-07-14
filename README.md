# Rotating Cube
A terminal-based 3D cube renderer built with Python. It uses ASCII characters to animate a spinning cube with realistic depth, rotation, and lighting effects.

----------

## Overview
This project is a simple introduction to 3D graphics. It covers the basics of 3D rotation, perspective projection, and lighting — all rendered directly in your terminal using text.

Originally built to demonstrate edge connections and cube rotation, the project now includes basic lighting and shading based on surface normals and light direction.

----------

## Key Concepts

### 3D Rotation
Each vertex of the cube is rotated around the X, Y, and Z axes using standard rotation matrices. This creates the spinning effect as the cube is animated over time.

### Perspective Projection
Once rotated, each 3D point is projected onto a 2D plane to simulate depth. Objects farther away appear smaller, mimicking how we see things in the real world.

### Lighting & Shading (New)
Each face of the cube is shaded based on:

-   The angle between the face and the light source
    
-   The distance from the light source
    

This gives the cube a more three-dimensional appearance, with light-facing surfaces appearing brighter and others darker.

----------

## ASCII Shading

The shading is displayed using a small set of ASCII characters, ordered from light to dark:

```
* 0 @ #
```
Each character is chosen based on the calculated light intensity on that face.

----------
## Math

### Rotation Matrices

Each cube vertex is rotated in 3D space using combined rotation matrices for the X, Y, and Z axes.

-   **Rotation around X-axis** (Roll):
    
		   `[ 1	0	 	 0 		]`
		   `[ 0	cos(θ)	-sin(θ) ]`
		   `[ 0	sin(θ)	 cos(θ) ]` 
    
-   **Rotation around Y-axis** (Pitch):
    
		    `[ cos(β)		0	 sin(β) ]`
		    `[ 0			1	 0 		]`
		    `[ -sin(β)	0	 cos(β) 	]` 
		    
-   **Rotation around Z-axis** (Yaw):
    
		   `[ cos(α)		-sin(α)		0 ]`
		   `[ sin(α)		cos(α)		0 ]`
		   `[ 0				1 			0 ]`
    

These are combined into a single rotation matrix applied to each 3D point.

----------

### Perspective Projection

To simulate depth, 3D coordinates are projected to 2D using this formula:

`projected_x = (width / 2) + (x * scale * aspect_ratio) / (z + distance)
projected_y = (height / 2) - (y * scale) / (z + distance)` 

-   `width` and `height`: Terminal screen size
    
-   `scale`: Controls overall size
    
-   `z + distance`: Ensures that closer points appear larger

----------

### Surface Normals

Each face has a surface normal calculated using the cross product of two vectors formed by its vertices:

`normal = np.cross(v2 - v1, v3 - v1)` 

The normal vector is then normalized (scaled to unit length) and used to determine how much light hits the face.

----------

### Light Intensity

Lighting is based on Lambertian reflection, where intensity is proportional to the cosine of the angle between the light direction and the face normal.


`intensity = (dot(normal, light_dir) / distance^1.5) * 3` 

-   `dot(normal, light_dir)`: Measures how directly the face faces the light
    
-   `distance^1.5`: Dims light based on distance
    
-   The intensity is clamped between 0 and 1 and mapped to an ASCII character
----------
## How It Works

-   `rotate()` – Rotates a 3D point around all three axes.
    
-   `project()` – Converts 3D coordinates to 2D screen space.
    
-   `get_normal()` – Calculates the normal vector for a face.
    
-   `get_intensity()` – Determines how bright a face should be based on light direction and distance.
    
-   `fill_face()` – Fills each cube face with the appropriate ASCII character based on intensity.
    
-   `draw_edges()` – Draws the cube's wireframe over the shaded faces.
