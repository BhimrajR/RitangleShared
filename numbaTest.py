from numba import cuda
import numpy as np
import math

@cuda.jit
def calculate_circle_0_points_kernel(a, b, r, edge_result, internal_result):
    x, y = cuda.grid(2)

    r_max = math.ceil(r)+1
    if x < r_max and y < r_max:
        if (x-a)**2 + (y-b)**2 <= r**2:
            if x == 0 or y == 0:
                cuda.atomic.add(edge_result, 0, 1)
            else:
                cuda.atomic.add(internal_result, 0, 1)


@cuda.jit
def calculate_circle_1_points_kernel(a, b, r, x_range, y_range, is_a_int, is_b_int, edge_result, internal_result):
    x, y = cuda.grid(2)

    if x < x_range and y < r_range:
        if (x-a)**2+(y-b)**2<=r**2:
            if is_a_int and x == int(a) or is_b_int and y == int(b):
                cuda.atomic.add(edge_result, 0, 1)
            else:
                cuda.atomic.add(internal_result, 0, 1)


@cuda.jit
def calculate_circle_2_points_kernel(a, b, r, x_range, y_range, is_b_int, edge_result, internal_result):
    x, y = cuda.grid(2)

    if x < x_range and y < r_range:
        if (x-a)**2+(y-b)**2<=r**2:
            if is_b_int and y == int(b):
                cuda.atomic.add(edge_result, 0, 1)
            else:
                cuda.atomic.add(internal_result, 0, 1)

@cuda.jit
def calculate_circle_3_points_kernel(a, b, r, x_range, y_range, edge_result, internal_result):
    x, y = cuda.grid(2)

    if x < x_range and y < r_range:
        if (x-a)**2+(y-b)**2<=r**2:
            if y == 0:
                cuda.atomic.add(edge_result, 0, 1)
            else:
                cuda.atomic.add(internal_result, 0, 1)



def calculate_circle_0_points_gpu(circle):
    a, b, r, _ = circle    
    edge_result = cuda.to_device(np.array([0], dtype=np.int32))
    internal_result = cuda.to_device(np.array([0], dtype=np.int32))

    threads_per_block = (16, 16)
    r_max = math.ceil(r) + 1
    blocks_per_grid_x = math.ceil(r_max / threads_per_block[0])
    blocks_per_grid_y = math.ceil(r_max / threads_per_block[1])
    blocks_per_grid = (blocks_per_grid_x, blocks_per_grid_y)

    calculate_circle_0_points_kernel[blocks_per_grid, threads_per_block](a, b, r, edge_result, internal_result)

    edge = edge_result.copy_to_host()[0] - 1
    internal = internal_result.copy_to_host()[0]
    return edge, internal


print(list(cuda.gpus)[0])

# print(calculate_circle_0_points_gpu((0,0,100,1)))


def calculate_circle_0_points(circle):
    a, b, r, _ = circle
    edge, internal = 0, 0
    
    r_max = math.ceil(r) + 1

    for x in range(r_max):
        for y in range(r_max):
            if (x-a)**2+(y-b)**2<=r**2:
                if x == 0 or y == 0:
                    edge += 1
                    continue
                internal += 1
    return edge - 1, internal

def calculate_circle_1_points(circle):
    a, b, r, _ = circle
    edge, internal = 0, 0
    
    x_min, x_max = int(a - r) - 1, int(a)+1
    y_min, y_max = int(b - r) - 1, int(b)+1

    is_a_int = a == int(a)
    is_b_int = b % 1 == 0
    for x in range(x_min, x_max):
        for y in range(y_min, y_max):
            if (x-a)**2+(y-b)**2<=r**2:
                if is_a_int and x == int(a) or is_b_int and y == int(b):
                    edge += 1
                    continue
                internal += 1
    
    if is_a_int and is_b_int: edge -= 1
    
    return edge, internal

def calculate_circle_2_points(circle):
    a, b, r, _ = circle
    edge, internal = 0, 0
    
    x_min, x_max = int(a - r), math.ceil(a+r)+1
    y_min, y_max = int(b - r), int(b)+1
    is_b_int = b % 1 == 0
    print(b)
    for x in range(x_min, x_max):
        for y in range(y_min, y_max):
            if (x-a)**2+(y-b)**2<=r**2:
                if is_b_int and y == int(b):
                    edge += 1
                    continue
                internal += 1
    return edge, internal

def calculate_circle_3_points(circle):
    a, b, r, _ = circle
    edge, internal = 0, 0
    
    x_min, x_max = int(a - r), math.ceil(a+r)+1
    y_min, y_max = 0, math.ceil(r)+1

    for x in range(x_min, x_max):
        for y in range(y_min, y_max):
            if (x-a)**2+(y-b)**2<=r**2:
                if y == 0:
                    edge += 1
                    continue
                internal += 1
    return edge, internal