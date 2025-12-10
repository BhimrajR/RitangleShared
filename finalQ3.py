from sympy import *
import math



x, y, r = symbols('x y r')

def devolverEcuacion(x1, y1, r1):
  # Definir la ecuación original
  ecuacion_original = (x - x1)**2 + (y - y1)**2 - (r + r1)**2
  # Expandir los cuadrados
  ecuacion_expandida = expand(ecuacion_original)
  # Simplificar términos semejantes
  ecuacion_simplificada = collect(ecuacion_expandida, [x, y, r])
  eq = Eq(ecuacion_simplificada, 0)
  return eq

def find_r2(circle1, circle2, circle3):
  # Datos del primer círculo
  x1 = circle1[0]
  y1 = circle1[1]
  r1 = circle1[2]

  x2 = circle2[0]
  y2 = circle2[1]
  r2 = circle2[2]

  x3 = circle3[0]
  y3 = circle3[1]
  r3 = circle3[2]

  eq1 = devolverEcuacion(x1, y1, r1)

  # Datos del segundo círculo
  eq2 = devolverEcuacion(x2, y2, r2)

  # Datos del tercer círculo
  eq3 = devolverEcuacion(x3, y3, r3)

  # Resolver el sistema de ecuaciones numéricamente
  sol = solve((eq1, eq2, eq3), (r, x, y), dict=True)

  for solution in sol:
      if solution[r] > 0:
          return solution[x], solution[y], solution[r]

def generate_inital_circles(Rx, Ry): # Generate the large and medium circles
    # Generate the largest circles
    circles = []
  
    r = min([math.sqrt(Rx**2+Ry**2)/4, Rx/2, Ry/2])

    circles.append((0, 0, r, 0.25))
    circles.append((Rx/2, Ry/2, r, 0.25))

    # Generate the medium circles

    circle1 = list(find_r2(circles[0], circles[1], (0, Ry, r)))
    circle2 = (circles[1][0]-circle1[0], 0, circle1[2], 0.5)
    circle1.append(0.5)
    circles.append(tuple(circle1))
    circles.append(circle2)

    return circles

def generate_unit_cell(Rx, Ry): # Generate the unit cell vertices
  unit_cell_vertices = [(0, 0), (0, Ry/2), (Rx/2, Ry/2), (Rx/2, 0)]
  return unit_cell_vertices

def float_digits(number, decimal_count): # Returns the scale to be an integer
    for i in range(1, (10**decimal_count)+1):
        temp = number*i
        if temp%1 == 0:
            k = i
            break
    return k

def calculate_vertex_count(unit_cell): # Count the number of points on a vertex
    vertex_count = 0

    for i in unit_cell:
        x = i[0]
        y = i[1]

        if x%1 == 0 and y%1 == 0:
            vertex_count += 1
    return vertex_count

def calculate_edge_count(unit_cell): # Count the number
    cell_width, cell_height = unit_cell[2]
    left_edge, bottom_edge = math.ceil(cell_height - 1), math.ceil(cell_width - 1)
    left_coef, bottom_coef = 2 if cell_width%1==0 else 1, 2 if cell_height%1==0 else 1
    return left_edge * left_coef + bottom_edge * bottom_coef

def calculate_internal_count(unit_cell):
    cell_width, cell_height = unit_cell[2]
    return math.ceil(cell_width - 1) * math.ceil(cell_height - 1)

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

def calculate_total_circle_points(circle_points):
    total_edge, total_internal = 0, 0
    for edge_points, internal_points in circle_points:
        total_edge += edge_points
        total_internal += internal_points
    return total_edge, total_internal

def circle_01_tangent(unit_cell):
    cell_width, cell_height = unit_cell[2]
    return cell_width % 2 == 0 and cell_height % 2 == 0

def circle_02_tangent(unit_cell, circles):
    dx, dy = circles[2][0], circles[2][1]
    r_ratio = circles[0][2] / (circles[0][2] + circles[2][2])
    return dx * r_ratio % 1 == 0 and dy * r_ratio % 1 == 0 

def circle_12_tangent(unit_cell, circles):
    return (circles[1][0] - circles[1][2]) % 1 == 0

def circle_03_tangent(unit_cell, circles):
    return circles[0][2] % 1 == 0

def circle_13_tangent(unit_cell, circles):
    dx, dy = (circles[1][0] - circles[3][0]), (circles[1][1] - circles[3][1])
    r_ratio = circles[3][2] / (circles[1][2] + circles[3][2])
    return (dx * r_ratio + circles[3][0]) % 1 == 0 and (dy * r_ratio + circles[3][1]) % 1 == 0 

def make_four_divide_Rx(Rx):
    while Rx%4 != 0:
        Rx += 1
    return Rx

def solve_max_p(width):
    decimal_count = len(str(width).split('.')[1])
    width_scale_factor = float_digits(width, decimal_count)

    for i in range(1, 1 + 1):
        Rx = int(width*width_scale_factor*i)
        Ry = int(width_scale_factor*i)
        print("A")
        unit_cell = generate_unit_cell(Rx, Ry)

        circles = generate_inital_circles(Rx, Ry)
        print("B")
        vertex_count = calculate_vertex_count(unit_cell)
        edge_count = calculate_edge_count(unit_cell)
        internal_count = calculate_internal_count(unit_cell)
        print(vertex_count, edge_count, internal_count)
        print("C")
        print((Rx,Ry), int((10**decimal_count)/width_scale_factor))
        circle_0_points = calculate_circle_0_points(circles[0])
        print("Alpha")
        circle_1_points = calculate_circle_1_points(circles[1])
        print("Beta")
        circle_2_points = calculate_circle_2_points(circles[2])
        print("Gamma")
        circle_3_points = calculate_circle_3_points(circles[3])
        print("Delta")



        print("D")

        total_circles_edge, total_circles_internal = calculate_total_circle_points([circle_0_points, circle_1_points, circle_2_points, circle_3_points])

        if circle_01_tangent(unit_cell): total_circles_internal -= 1 
        
        if circle_02_tangent(unit_cell, circles): total_circles_internal -= 1 
        if circle_12_tangent(unit_cell, circles): total_circles_edge -= 1 
        
        if circle_03_tangent(unit_cell, circles): total_circles_edge -= 1 
        if circle_13_tangent(unit_cell, circles): total_circles_internal -= 1 

        print("E")

        minis_edge, minis_internal = edge_count - total_circles_edge, internal_count - total_circles_internal

        p_numerator = 0.25 * vertex_count + 0.5 * edge_count + internal_count
        p_denominator = 1.5 + 0.5 * minis_edge + minis_internal

        p = p_numerator / p_denominator

        print(minis_edge, minis_internal)

        print(unit_cell, internal_count)

        print(p)

Rx, Ry = 14189, 8192
print("A")
unit_cell = generate_unit_cell(Rx, Ry)

circles = generate_inital_circles(Rx, Ry)
print("B")
vertex_count = calculate_vertex_count(unit_cell)
edge_count = calculate_edge_count(unit_cell)
internal_count = calculate_internal_count(unit_cell)
print(vertex_count, edge_count, internal_count)
print("C")

circle_0_points = calculate_circle_0_points(circles[0])
print("Alpha")
circle_1_points = calculate_circle_1_points(circles[1])
print("Beta")
circle_2_points = calculate_circle_2_points(circles[2])
print("Gamma")
circle_3_points = calculate_circle_3_points(circles[3])
print("Delta")
print(circles)
print(circle_0_points, circle_1_points, circle_2_points, circle_3_points)

print("D")

total_circles_edge, total_circles_internal = calculate_total_circle_points([circle_0_points, circle_1_points, circle_2_points, circle_3_points])

if circle_01_tangent(unit_cell): total_circles_internal -= 1 

if circle_02_tangent(unit_cell, circles): total_circles_internal -= 1 
if circle_12_tangent(unit_cell, circles): total_circles_edge -= 1 

if circle_03_tangent(unit_cell, circles): total_circles_edge -= 1 
if circle_13_tangent(unit_cell, circles): total_circles_internal -= 1 

print("E")

minis_edge, minis_internal = edge_count - total_circles_edge, internal_count - total_circles_internal

p_numerator = 0.25 * vertex_count + 0.5 * edge_count + internal_count
p_denominator = 1.5 + 0.5 * minis_edge + minis_internal

p = p_numerator / p_denominator

print(minis_edge, minis_internal)

print(unit_cell, internal_count)

print(p)


# solve_max_p(1.73205)

