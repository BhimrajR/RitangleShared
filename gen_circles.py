from sympy import *

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

def generate_starting_params(R):
  circles = []

  r1 = R*5/8

  circles.append((0, 0, r1, 0.25))
  circles.append((R*3/2, 0, r1, 0.25))
  circles.append((R*3/4, R, r1, 0.5))

  x1, y1, r2 = find_r2(circles[0], circles[1], circles[2])

  circles.append((x1, y1, r2, 1))
  circles.append((0, R*5/8+r2, r2, 0.5))
  circles.append((R*3/2, R*5/8+r2, r2, 0.5))

  unit_cell_vertices = [(0, 0), (0, R), (R*3/2, R), (R*3/2, 0)]

  return unit_cell_vertices, circles