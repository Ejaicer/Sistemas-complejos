import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

###########33 Parámetros
T = 30.0
tiempos = np.linspace(0, T, 3000)

####################### Atractor de Lorenz
sigma = 10.0
beta_l = 8.0/3.0
rho = 28.0

def al(t, u):
    x, y, z = u
    return np.array([sigma * (y - x), x * (rho - z) - y, x * y - beta_l * z])

##############3 Perturbación de las condiciones iniciales sobre x
u0 = [2.0, 1.0, 0.5]
epsilon = 1e-3
u0_p = [2.0 + epsilon, 1.0, 0.5] #### ci perturbadas

sol_l1 = solve_ivp(al, (0, T), u0, method="RK45", t_eval=tiempos, rtol=1e-8, atol=1e-10)
sol_l2 = solve_ivp(al, (0, T), u0_p, method="RK45", t_eval=tiempos, rtol=1e-8, atol=1e-10)

############### soluciones
plt.figure(figsize=(10, 4))
plt.plot(sol_l1.t, sol_l1.y[0], label=f"u0 = {u0}", color="darkcyan")
plt.plot(sol_l2.t, sol_l2.y[0], label=f"u0_p = {u0_p}", color="salmon", linestyle="-.")
plt.xlabel("Tiempo (t)")
plt.ylabel("x(t)")
plt.title("Sensibilidad a Condiciones Iniciales en Lorenz (Variable x)")
plt.legend()
plt.grid(True)
plt.show()

##############  graficas sol particulares, espacio fase
u1 = [2.0,1.0,0.5]
u2 = [-1.0,0.5,1.0]
cip = [u0, u1, u2] # [theta0, omega0]


for i in cip:
##########################3 (x,y)

    solxy = solve_ivp(al, (0, T), i, method="RK45", t_eval=tiempos, rtol=1e-8, atol=1e-10)
    plt.plot(solxy.y[0], solxy.y[1], label=f"x0={i[0]}, y0={i[1]}", color="darkcyan")


########## parámetros gráficas
#plt.xlim(-6,6)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Espacio de Fases: Lorenz-xy")
    plt.legend()
    plt.grid(True)
    plt.show()

##########################3 (x,z)

    solxz = solve_ivp(al, (0, T), i, method="RK45", t_eval=tiempos, rtol=1e-8, atol=1e-10)
    plt.plot(solxz.y[0], solxz.y[2], label=f"x0={i[0]}, z0={i[2]}", color="salmon")


########## parámetros gráficas
#plt.xlim(-6,6)
    plt.xlabel("x")
    plt.ylabel("z")
    plt.title("Espacio de Fases: Lorenz-xz")
    plt.legend()
    plt.grid(True)
    plt.show()

##########################3 (y,z)

    solyz = solve_ivp(al, (0, T), i, method="RK45", t_eval=tiempos, rtol=1e-8, atol=1e-10)
    plt.plot(solyz.y[1], solyz.y[2], label=f"y0={i[1]}, z0={i[2]}", color="olive")


########## parámetros gráficas
#plt.xlim(-6,6)
    plt.xlabel("y")
    plt.ylabel("z")
    plt.title("Espacio de Fases: Lorenz-yz")
    plt.legend()
    plt.grid(True)
    plt.show()

################ Espacio de fases 3d 
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
ax.plot(sol_l1.y[0], sol_l1.y[1], sol_l1.y[2], color="darkcyan", lw=0.6)
ax.plot(sol_l2.y[0], sol_l1.y[1], sol_l1.y[2], color="salmon", lw=0.6)
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.set_title("Atractor Caótico de Lorenz")
plt.show()