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
  print(eq)
  return eq


# Datos del primer círculo
x1, y1, r1 = 0, 0, 12.5
eq1 = devolverEcuacion(x1, y1, r1)

# Datos del segundo círculo
x2, y2, r2 = 30, 0, 12.5
eq2 = devolverEcuacion(x2, y2, r2)

# Datos del tercer círculo
x3, y3, r3 = 15, 20, 12.5
eq3 = devolverEcuacion(x3, y3, r3)

# Resolver el sistema de ecuaciones numéricamente
sol = solve((eq1, eq2, eq3), (r, x, y), dict=True)

# Imprimir la solución
print("Solución:")
print(sol)