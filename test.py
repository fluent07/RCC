from logging import error


# import sympy as s
# import numpy as np
# from rect_geometry import *
# import newton as n
# import newtonR as nr
# import matplotlib.pyplot as plt
# h = s.symbols('h')

def rect(width):
    # global area, wperimeter, hydraulic_radius, hydraulic_depth, depth_centroid
    area = lambda h: h * width
    wperimeter = lambda h: width + 2 * h
    hydraulic_radius = lambda h: area(h) / wperimeter(h)
    hydraulic_depth = lambda h: area(h) / width
    depth_centroid = lambda h: h / 2
    return area, wperimeter, hydraulic_radius, hydraulic_depth, depth_centroid


def Q_chezy(area_q, hydraulic_radius_q, ks, Sb):
    '''global velocity, discharge'''
    velocity = lambda h: ks * hydraulic_radius_q(h) ** (2 / 3) * Sb ** (1 / 2)
    discharge = lambda h: area_q(h) * velocity(h)
    return velocity, discharge


def froude(area_f, hydraulic_depth_f, discharge_f):
    # global Fr
    g = 9.806
    Fr = lambda h: discharge_f / (area_f(h) * (g * hydraulic_depth_f(h)) ** 0.5)
    return Fr


def energy(area_e, discharge_e):
    # global piezometric_head, velocity_head, specific_energy
    g = 9.806
    piezometric_head = lambda h: h
    velocity_head = lambda h: (discharge_e ** 2) / (2 * g * area_e(h) ** 2)
    specific_energy = lambda h: piezometric_head(h) + velocity_head(h)
    return piezometric_head, velocity_head, specific_energy


def energy_slope(area_es, hydraulic_radius_es, ks_es, discharge_es):
    # global Sf
    Sf = lambda h: (discharge_es ** 2) / (area_es(h) ** 2 * ks_es ** 2 * (hydraulic_radius_es(h) ** (4 / 3)))
    return Sf


def specific_force(depth_centroid_sf, area_sf, discharge_sf, density_sf):
    # global pressure_force, momentum_flux, force
    g = 9.806
    gamma = density_sf * g  # specific weight
    pressure_force = lambda h: gamma * area_sf(h) * depth_centroid_sf(h)
    momentum_flux = lambda h: density_sf * discharge_sf ** 2 / area_sf(h)
    force = lambda h: pressure_force(h) + momentum_flux(h)
    return pressure_force, momentum_flux, force


def newtonR(f, x0):
    tolf = 1e-08  # tolerance on the value of f
    tolx = 1e-08  # tolerance of the amplitude of the [a b] interval
    dx = 1e-08
    df = lambda x: (f(x + dx) - f(x)) / dx
    # df = s.lambdify(var,df2)
    # f = s.lambdify(var, f2)
    iter_root = [x0]
    g = 1000
    k = 1
    while k < g:
        # print(x[0])
        iter_root.append((iter_root[k - 1]) - (f(iter_root[k - 1]) / df(iter_root[k - 1])));  # find the value of xk that makes the tangent to the function f = 0 at a certain step k
        # Check if we found a root in x(k):
        # a) yes if the value of the function f(x(k))  is less than the tolerance tolf 
        if abs(f(iter_root[k])) <= tolf:
            root = iter_root[k]
            return root
        # b) yes if the amplitude of the [x(k) x(k-1)] interval is less than the tolerance tolx
        elif abs(iter_root[k] - iter_root[k - 1]) <= tolx:
            root = iter_root[k]
            return root
        k += 1
        # 2. In case no roots were found after N iterations, print an error message
    if k == g:
        error("The method does not converge")

        # return k

# Q = 9
# b2 = 7
# Sb = 0.0006
# ks2 = 55.55

# area1, wperimeter1, hydraulic_radius1, hydraulic_depth1, depth_centroid1 = rect(b2)
# velocity1, discharge1 = Q_chezy(area1, hydraulic_radius1,ks2,Sb)
# fh0 = lambda h: discharge1(h)-Q
# h0 = newtonR(fh0,1)
# print(h0)
# print(discharge1(h0),"HR is",hydraulic_radius1(h0))
