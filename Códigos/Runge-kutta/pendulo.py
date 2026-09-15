#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 14:55:13 2026

@author: ejaicer
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

################# parámetros
T = 30.0
tiempos = np.linspace(0, T, 3000)

#########################3 péndulo simple
g = 9.81
ell = 2

def pendulo(t, u):
    theta, omega = u
    return np.array([omega, -(g / ell) * np.sin(theta)])

######################## Espacio de las fases
Theta, Omega = np.meshgrid(np.linspace(-2*np.pi, 2*np.pi, 25), np.linspace(-8, 8, 25))
F_p = Omega
G_p = -(g / ell) * np.sin(Theta)
norma_p = np.hypot(F_p, G_p)

plt.figure(figsize=(9, 6))
plt.quiver(Theta, Omega, F_p / np.where(norma_p > 0, norma_p, 1), G_p / np.where(norma_p > 0, norma_p, 1), angles="xy", alpha=0.3)

##############  graficas sol particulares, espacio fase
cip = [[0.5, 0.0], [-6, 6.3], [0.0, 5.0]] # [theta0, omega0]
for u0 in cip:
    sol = solve_ivp(pendulo, (0, T), u0, method="RK45", t_eval=tiempos, rtol=1e-8, atol=1e-10)
    plt.plot(sol.y[0], sol.y[1], label=f"CI: θ0={u0[0]}, ω0={u0[1]}")


########## parámetros gráfica espacio fase
plt.xlim(-6,6)
plt.xlabel("Ángulo θ (rad)")
plt.ylabel("Velocidad Angular ω (rad/s)")
plt.title("Espacio de Fases: Péndulo Simple")
plt.legend()
plt.grid(True)
plt.show()

#################### evolución temporal

for i in cip:
    
############################## ángulo
    U = solve_ivp(pendulo, (0, T), i, method="RK45", t_eval=tiempos, rtol=1e-8, atol=1e-10)
    plt.figure(figsize=(6, 4))
    plt.plot(U.t, U.y[0], label="ángulo", color="cadetblue")
    plt.xlim(0,30)
    plt.xlabel("Tiempo (t)")
    plt.ylabel("ángulo")
    plt.title(fr"Evolución Temporal péndulo; ($\theta_{0}$,$\omega_{0}$)={i}")
    plt.grid(True)
    plt.show()

################################## velocidad ángular

    Uw = solve_ivp(pendulo, (0, T), i, method="RK45", t_eval=tiempos, rtol=1e-8, atol=1e-10)
    plt.figure(figsize=(6, 4))
    plt.plot(Uw.t, Uw.y[1], label="velocidad angular", color="plum")
    plt.xlim(0,30)
    plt.xlabel("Tiempo (t)")
    plt.ylabel("velocidad angular")
    plt.title(fr"Evolución Temporal péndulo; ($\theta_{0}$,$\omega_{0}$)={i}")
    plt.grid(True)
    plt.show()
