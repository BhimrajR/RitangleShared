#this code only works for quadrelaterals
import copy
import math
from gen_circles import *
import numpy as np
import matplotlib.pyplot as plt

def get_min_max_x_y(unit_cell_vertices):
    min_x = 1000000
    max_x = -1000000
    min_y = 1000000
    max_y = -1000000
    
    for i in unit_cell_vertices:
        if i[1]<min_y:
            min_y = i[1]
        if i[0]<min_x:
            min_x = i[0]
        if i[1]>max_y:
            max_y = i[1]
        if i[0]>max_x:
            max_x = i[0]

    return min_x, max_x, min_y, max_y

def make_line(x1, y1, x2, y2):
    m = (y1-y2)/(x1-x2)
    c = y1-m*x1
    return m, c

def make_check(unit_cell_vertices):
    checks_internal = []
    checks_edge = []
    checks_all = []
    
    for i in range(-1, len(unit_cell_vertices)-1):
        point1 = unit_cell_vertices[i]
        point2 = unit_cell_vertices[i+1]

        x1 = point1[0]
        y1 = point1[1]
        x2 = point2[0]
        y2 = point2[1]

        m = 0
        c = 0
        
        if x1 == x2:
            temp = f"x-{x2}"
        else:
            m, c = make_line(x1, y1, x2, y2)
            if c!=0 and m!=0:
                temp = f"{m}*x+{c}-y"
            elif c == 0 and m!=0:
                temp = f"{m}*x-y"
            elif c!=0 and m==0:
                temp = f"{c}-y"
            else:
                temp = f"-y"

        temp_arr = copy.deepcopy(unit_cell_vertices)
        temp_arr.remove(point1)
        temp_arr.remove(point2)

        temp2 = temp+"==0"
        temp3 = temp
        for j in temp_arr:
            x = j[0]
            y = j[1]
            k = eval(temp)
            if k == 0:
                continue
            if k < 0:
                temp+="<0"
                temp3 += "<=0"
                break
            if k > 0:
                temp+=">0"
                temp3 += ">=0"
                break
        checks_internal.append(temp)
        checks_edge.append(temp2)
        checks_all.append(temp3)

    return checks_internal, checks_edge, checks_all

def check_internal(point, check):
    x = point[0]
    y = point[1]

    counter = 0
    for statement in check:
        if eval(statement):
            counter+=1
    if counter == len(check):
        return True
    else:
        return False

def check_edge(point, check):
    x = point[0]
    y = point[1]

    counter = 0
    for statement in check:
        if eval(statement):
            counter+=1
    if counter >= 1:
        return True
    else:
        return False

def points_in_cell(unit_cell_vertices):
    mins_and_maxes = get_min_max_x_y(unit_cell_vertices)

    min_x = math.floor(mins_and_maxes[0])
    max_x = math.ceil(mins_and_maxes[1])
    min_y = math.floor(mins_and_maxes[2])
    max_y = math.ceil(mins_and_maxes[3])

    check = make_check(unit_cell_vertices)

    internal_points = []
    edge_points = []
    all_points = []

    for x in range(min_x, max_x+1):
        for y in range(min_y, max_y+1):
            if check_internal([x, y], check[0]):
                internal_points.append([x, y])
                all_points.append([x, y])
            elif check_edge([x, y], check[1]) and check_internal([x, y], check[2]):
                edge_points.append([x, y])
                all_points.append([x, y])

    for i in unit_cell_vertices:
        if list(i) in edge_points:
            edge_points.remove(list(i))
    
    vertex_points = []

    for i in unit_cell_vertices:
        x = i[0]
        y = i[1]

        if x%1 == 0 and y%1 == 0:
            vertex_points.append(list(i))

    return internal_points, edge_points, vertex_points, all_points

def find_p_numerator(internal_points, edge_points, vertex_points):
    return len(internal_points) + 0.5*len(edge_points) + 0.25*len(vertex_points)

def points_in_circle(circle, points):
    a = circle[0]
    b = circle[1]
    r = circle[2]
    
    inpoints = []
    for i in points:
        x = i[0]
        y = i[1]
        if (x-a)**2+(y-b)**2<=r**2:
                inpoints.append(i)
    return inpoints

def find_p_denominator(circles):
    tot = 0
    for circle in circles:
        tot += circle[3]
    return tot

def find_p_denominator_mini_circles(circles, internal_minis, edge_minis, vertex_minis):
    p_denominator = find_p_denominator(circles)
    p_denominator += len(internal_minis) + len(edge_minis)*0.5 + len(vertex_minis)*0.25
    return p_denominator

def get_arrs_from_text():
    unit_cell_vertices = []
    circles = []

    f = open(r"test.txt")
    strng = f.read()
    arr = strng.splitlines()

    counter = 0
    for i in arr:
        if i == "":
            counter += 1
    for i in range(counter):
        arr.remove("")

    loops = int(arr[0])
    arr = arr[1::]
    for i in range(loops):
        unit_cell_vertices.append(eval(f"({arr[0]})"))
        arr  =arr[1::]

    loops = int(arr[0])
    arr = arr[1::]
    for i in range(loops):
        circles.append(eval(f"({arr[0]})"))
        arr  =arr[1::]

    return unit_cell_vertices, circles

def find_q(circles, unit_cell_vertices):
    circle_A = 0
    for circle in circles:
        circle_A += math.pi*(circle[2]**2)*circle[3]
    
    polygon_A = 0

    for i in range(-1, len(unit_cell_vertices)-1):
        point1 = unit_cell_vertices[i]
        point2 = unit_cell_vertices[i+1]

        x1 = point1[0]
        y1 = point1[1]
        x2 = point2[0]
        y2 = point2[1]

        polygon_A += (x1-x2)*(y1-y2)
    return circle_A/polygon_A

def find_mini_circles(circles, internal_points, edge_points, vertex_points, all_points):
    all_points_copy = copy.deepcopy(all_points)
    edge_points_copy = copy.deepcopy(edge_points)
    vertex_points_copy = copy.deepcopy(vertex_points)
    internal_points_copy = copy.deepcopy(internal_points)
    

    for circle in circles:
        inpoints = points_in_circle(circle, all_points_copy)
        for i in inpoints:
            all_points_copy.remove(i)
            if i in internal_points:
                internal_points_copy.remove(i)
            elif i in edge_points:
                edge_points_copy.remove(i)
            elif i in vertex_points:
                vertex_points_copy.remove(i)
    return internal_points_copy, edge_points_copy, vertex_points_copy, all_points_copy

max = [0, 0, 0]
x = np.array([])
y = np.array([])

width = 1.73
print(width)

print("started search")
for i in range(1, 100+1):
    temp = width*i
    if temp%1 == 0:
        k = i
        break
print(100/k)

for j in range(1, int(100/k)+1):
    max2 = 0
    Rx = int(width*k*j)
    Ry = int(k*j)
    unit_cell_vertices, circles = generate_starting_params_general(Rx, Ry)

    circles = generate_wide_circles(Rx, Ry, circles)

    internal_points, edge_points, vertex_points, all_points = points_in_cell(unit_cell_vertices)
    no_points = len(all_points)

    internal_minis, edge_minis, vertex_minis, all_minis = find_mini_circles(circles, internal_points, edge_points, vertex_points, all_points)
    print(len(internal_minis), len(edge_minis))


    # p_numerator = find_p_numerator(internal_points, edge_points, vertex_points)
    # p_denominator = find_p_denominator_mini_circles(circles, internal_minis, edge_minis, vertex_minis)
    # p = p_numerator/p_denominator
    # if p>max2:
    #     max2 = copy.deepcopy(p)
    # if p > max[2]:
    #     max = [Rx, Ry, p, p_numerator, p_denominator, width]
    #     max_circles = copy.deepcopy(circles)
    # np.append(x, j)
    # np.append(y, max2)
    # print(f"done with {j}")

    # print(max)
print(max_circles)
print(edge_points)
print(vertex_points)
plt.scatter(x, y)
plt.show()

# # unit_cell_vertices, temp = get_arrs_from_text()

# internal_points, edge_points, vertex_points, all_points = points_in_cell(unit_cell_vertices)
# print(len(internal_points))
# # print(f"{internal_points}\n\n{edge_points}\n\n{vertex_points}")

# no_points = len(all_points)
# # print(no_points)

# # bunch of print statements to test stuff, it works i promise

# # print(unit_cell_vertices)
# # print(circles)

# internal_minis, edge_minis, vertex_minis, all_minis = find_mini_circles(circles, internal_points, edge_points, vertex_points, all_points)
# print(len(internal_points))
# p_numerator = find_p_numerator(internal_points, edge_points, vertex_points)
# p_denominator = find_p_denominator_mini_circles(circles, internal_minis, edge_minis, vertex_minis)
# p = p_numerator/p_denominator
# print(p, p_numerator, p_denominator)

# print("")
# print(internal_points)
# print(edge_points)
# print(vertex_points)
# print(all_points)
# print(no_points)
# print(find_p_numerator(internal_points, edge_points, vertex_points)/find_p_denominator(circles))
# print(find_q(circles, unit_cell_vertices))
