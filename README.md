# RotatingCube

![simplescreenrecorder](https://github.com/user-attachments/assets/8b0a76e5-27aa-4e2e-aa92-988778eeb80e)

This Python script renders a spinning 3D cube directly in the terminal. It's an introduction to the fundamental concepts of 3D computer graphics.

## Purpose: An Introduction to 3D Graphics

The main goal of this project is to get a hands-on learning experience about how 3D graphics work.

## The Math

At its core, making a 3D object appear on a 2D screen involves two main steps: rotating the object in 3D space and then projecting it onto the 2D screen.

### Vertices and Edges: 

*   **Vertices:** The corners of the cube. In this code, `vertices` is a list of points, where each point has an X, Y, and Z coordinate. These coordinates define the cube's position in a 3D space.
*   **Edges:** These are the lines that connect the corners (vertices) of the cube.

### Rotating the Cube in 3D Space

To make the cube spin, we need to continuously update the position of its vertices. This is done using a mathematical tool called a **rotation matrix**. A rotation matrix is a grid of numbers that, when applied to a point's coordinates, gives you its new coordinates after being rotated around a certain axis.

Our `rotate` function does exactly this. It takes a point's `(x, y, z)` coordinates and rotation angles for each axis (`ax`, `ay`, `az`) and calculates the new position.

#### The Rotation Formula

The code combines rotations around the X, Y, and Z axes into one matrix:

*   **Rotation around the X-axis (Roll):**
    ```
      [ 1,  0,       0      ]
      [ 0,  cos(θ), -sin(θ) ]
      [ 0,  sin(θ),  cos(θ) ]
    ```
*   **Rotation around the Y-axis (Pitch):**
    ```
      [ cos(β),  0,  sin(β) ]
      [ 0,       1,  0      ]
      [-sin(β),  0,  cos(β) ]
    ```
*   **Rotation around the Z-axis (Yaw):**
    ```      [ cos(α), -sin(α), 0 ]
      [ sin(α),  cos(α), 0 ]
      [ 0,       0,      1 ]
    ```
The script's `rotation_matrix` is a combination of these principles to apply rotation around all three axes simultaneously.

### Projecting a 3D Object onto a 2D Screen

Once our cube is rotated in its 3D world, we need to figure out how to represent it on our flat 2D screen. This is where **perspective projection** comes in.

Think about how you see the world. Objects that are farther away appear smaller, and objects that are closer look bigger. Perspective projection mimics this effect.

#### The Projection Formula

Our `project` function uses a simple formula to achieve this:

*   `projected_x = (width / 2) + (x * scale) / (z + distance)`
*   `projected_y = (height / 2) - (y * scale) / (z + distance)`

Let's break it down:

*   `(width / 2)` and `(height / 2)` are used to center the object on our screen.
*   `x * scale` and `y * scale` are used to make the object larger or smaller.
*   The most important part is dividing by `(z + distance)`. The `z` coordinate represents how "deep" into the screen the point is. By dividing by a value related to `z`, points with a larger `z` (farther away) will have their `x` and `y` values reduced, making them appear smaller and closer to the center of the screen. This creates the illusion of depth.

## Code Overview

*   **`rotate(x, y, z, ax, ay, az)`**: Takes a 3D point and rotation angles and returns the new coordinates of the point after rotation.
*   **`project(x, y, z, width, height, scale, distance)`**: Takes a 3D point and converts it into 2D coordinates for our screen.
*   **`draw_points(screen)`**: Calculates the 2D projection for each vertex of the cube.
*   **`draw_edges(screen, edges, projected)`**: Draws the lines (edges) between the projected vertices on the screen using ASCII characters.
*   **The `while True` loop**: This is the main part of our program. It continuously clears the screen, rotates the cube, projects it, draws it, and then waits for a very short period before repeating. This rapid redrawing creates the smooth animation of a spinning cube.
