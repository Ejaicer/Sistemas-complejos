import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

############# Parámetros

T = 30.0
tiempos = np.linspace(0, T, 3000)

###########parámetros del modelo

alpha =1.2 #### tasa de crecimiento presas
beta = 0.3 #### muerte por depredación
delta = 0.1 #### crecimiento de depredadores
gamma = 0.2 #### muerte de depredadores


#############333 Lotka-Volterra

def lv(t, u):
    x, y = u
    return np.array([alpha * x - beta * x * y, delta * x * y - gamma * y])

################## Espacio de fases
xmax = 15
ymax = 14
X, Y = np.meshgrid(np.linspace(0.0, xmax, 25), np.linspace(0, ymax, 25))
F = alpha * X - beta * X * Y
G = delta * X * Y - gamma * Y
norma = np.hypot(F, G)

plt.figure(figsize=(8, 6))
plt.quiver(X, Y, F / np.where(norma > 0, norma, 1), G / np.where(norma > 0, norma, 1), angles="xy", alpha=0.3)

##############  graficas sol particulares, espacio fase
ci_lv = [[2.0, 1.0], [3.0, 7.0], [6.0, 2.0]] ### (xo,yo)
for u0 in ci_lv:
    sol = solve_ivp(lv, (0, T), u0, method="RK45", t_eval=tiempos, rtol=1e-8, atol=1e-10)
    plt.plot(sol.y[0], sol.y[1], label=f"CI: x0={u0[0]}, y0={u0[1]}")
    
#######################parámetros gráficas espacio fase
plt.ylim(0,ymax)
plt.xlim(0,xmax)
plt.xlabel("Presas")
plt.ylabel("Depredadores")
plt.title("Espacio de Fases: Lotka-Volterra")
plt.legend()
plt.grid(True)
plt.show()

#################### evolución temporal

for i in ci_lv:
    U = solve_ivp(lv, (0, T), i, method="RK45", t_eval=tiempos, rtol=1e-8, atol=1e-10)
    plt.figure(figsize=(10, 4))
    
    plt.plot(U.t, U.y[0], label="Presas", color="cadetblue")
    plt.plot(U.t, U.y[1], label="Depredadores", color="plum")
    plt.xlim(0,30)
    plt.xlabel("Tiempo (t)")
    plt.ylabel("Población")
    plt.title(f"Evolución Temporal Lotka-Volterra; x0={i}")
    plt.legend()
    plt.grid(True)
    plt.show()
