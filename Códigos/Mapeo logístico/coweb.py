#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 20:55:10 2026

@author: ejaicer
"""
######### módulos
import numpy as np
import matplotlib.pyplot as plt

########### Parámetros
a = 3.6
x0 = 0.2
n_iter = 100

############# mapeo logístico
def ml(x):
    return a * x * (1 - x)

# Curvas
x = np.linspace(0, 1, 500)

plt.figure(figsize=(8, 8))

plt.plot(x, ml(x), label=fr"$f(x)= {a}x(1-x)$")
plt.plot(x, x, "k--", label=r"$y=x$")

########3 Cobweb
xn = x0

for i in range(n_iter):
    xn1 = ml(xn)

# Movimiento vertical: (xn, xn) -> (xn, xn1)
    plt.plot([xn, xn], [xn, xn1], "k-", linewidth=0.8)

# Movimiento horizontal: (xn, xn1) -> (xn1, xn1)
    plt.plot([xn, xn1], [xn1, xn1], "k-", linewidth=0.8)

    xn = xn1

plt.xlabel(r"$x_n$")
plt.ylabel(r"$x_{n+1}$")
plt.title(fr"Cobweb del mapeo logístico, $a={a}$")
plt.xlim(0, 1)
plt.ylim(0, 1)
plt.legend()
plt.grid()

plt.show()