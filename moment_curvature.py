import numpy as np
import matplotlib.pyplot as plt
import math as m

# --- Given Data ---
b = 300  # mm, width of section
h = 450 # mm, total height
c = 40  # mm, cover from top and bottom
d = h-c
# h = d + c  # mm, effective height of section
n = 7.51  # Modular ratio
tr = 25.4 # tension reinforcement
n_tr = 4 # no of tension reinforcement
cr = 25.4 # compression reinforcement
n_cr =2 # no of compression reinforcement
# Reinforcement details
# Asc = n_cr * (m.pi / 4) * cr**2  # Compression reinforcement area (mm^2)
# As = n_tr * (m.pi / 4) * tr**2  # Tension reinforcement area (mm^2)
As = 3039 # mm^2, tension reinforcement area (mm^2)
Asc = 1548 # mm^2, compression reinforcement area (mm^2)
# Material properties
f_ck = 25  # MPa, characteristic compressive strength of concrete
f_y =  276 # MPa, yield strength of steel
gamma_c = 1.5  # Safety factor for concrete
gamma_s = 1.15  # Safety factor for steel
alpha_cc = 0.85  # Concrete strength reduction factor
Es = 200000  # Young's modulus of steel

# Design strengths
fcd = alpha_cc * (f_ck / gamma_c)  # MPa
# fcd = 20.7  # MPa
fyd = f_y / gamma_s  # MPa


f_cm = f_ck + 8  # MPa, mean compressive strength of concrete
# Calculate modulus of elasticity of concrete (Ec) in MPa
Ec = 22 * ((f_cm / 10) ** 0.3) * 1000  # Convert GPa to MPa
print(f"Modulus of Elasticity of Concrete (Ec): {Ec} MPa")
Ct = 1.361
n = round(Es / Ec * ( 1 + Ct ),2) # Modular ratio
print("Modular ratio (n):", n)

# f_ctm = 0.3 * (f_ck ** (2 / 3))  # MPa, mean tensile strength of concrete

# Function to calculate neutral axis using Newton-Raphson
def newtonR(f, x0):
    tolf = 1e-08
    tolx = 1e-08
    dx = 1e-08
    df = lambda x: (f(x + dx) - f(x)) / dx
    iter_root = [x0]
    for k in range(1000):
        iter_root.append(iter_root[k] - (f(iter_root[k]) / df(iter_root[k])))
        if abs(f(iter_root[k + 1])) <= tolf or abs(iter_root[k + 1] - iter_root[k]) <= tolx:
            return iter_root[k + 1]
    raise ValueError("Newton-Raphson method did not converge.")

# --- Calculations ---
# Ultimate Neutral axis depth (x) from force equilibrium
x_ult = (As - Asc) * fyd / (0.8 * fcd * b)

# Design moment resistance (Mrd)
M_rd = As * fyd * (d - 0.4 * x_ult) / (10**6)  # Convert to kNm
M_rd2 = (fcd * 0.8 * x_ult * b * (d - 0.4 * x_ult) + fyd * Asc * (d - c)) * 1e-6

# Uncracked moment of inertia (I_uncr) - for a rectangular section
Eqn_NA_Uncracked = (
    lambda x_uncr: ((b * x_uncr**2) / 2)
    + (n * Asc * (x_uncr - c))
    - ((b * (h - x_uncr) ** 2) / 2)
    - (n * As * (d - x_uncr))
)
NA_uncracked = newtonR(Eqn_NA_Uncracked, 100)  # Neutral axis of uncracked section
# print("NA_uncracked:",NA_uncracked,"mm")

I_uncr = (
    (b / 3) * NA_uncracked**3
    + n * Asc * (NA_uncracked - c) ** 2
    + (b / 3) * (h - NA_uncracked) ** 3
    + n * As * (d - NA_uncracked) ** 2
)
I_uncr_in_inches = I_uncr / (25.4**4)  # Convert mm^4 to in^4
print("I_uncr:", I_uncr, "mm^4")
print("I_uncr:", I_uncr_in_inches, "in^4")


# Cracked moment of inertia (I_cr) - transformed section
Eqn_NA_cracked = lambda x_cr: (b * x_cr**2 / 2) + (n * Asc * (x_cr - c)) - (n * As * (d - x_cr))
NA_cracked = newtonR(Eqn_NA_cracked, 100)

# Parallel axis theorem to find I_cr
I_cr = (
    (b / 3) * NA_cracked**3
    + n * Asc * (NA_cracked - c) ** 2
    + n * As * (d - NA_cracked) ** 2
)  # (b * x**3) / 3 + (n * As * (d - y_n)**2) + (n * Asc * (y_n - c)**2)

# First moment of cracking (M_cr)
f_ctm = 0.3 * (f_ck ** (2 / 3))  # MPa, mean tensile strength of concrete
y = h / 2  # Distance to extreme fiber
f_ctm_psi = f_ctm * 145.038  # Convert MPa to psi
print("f_ctm:", f_ctm, "MPa")
print("f_ctm:", f_ctm_psi, "psi")
M_cr = (f_ctm * I_uncr) / (h - NA_uncracked) / (10**6)  # Convert to kNm

results = {
    "Neutral Axis (Uncracked)": (f"{NA_uncracked:.3f} mm", "((b * x_uncr^2) / 2)+(n * Asc * (x_uncr - c)) = ((b * (h - x_uncr)^2) / 2)+(n * As * (d - x_uncr))"),
    "Moment of Inertia (Uncracked)": (I_uncr, "(b / 3) * NA_uncracked^3 + n * Asc * (NA_uncracked - c)^2 + (b / 3) * (h - NA_uncracked)^3 + n * As * (d - NA_uncracked)^2"),
    "Neutral Axis (Cracked)": (f"{NA_cracked:.3f} mm", "(b * x_cr^2 / 2) + (n * Asc * (x_cr - c)) = (n * As * (d - x_cr))"),
    "Moment of Inertia (Cracked)": (I_cr, "(b / 3) * NA_cracked^3 + n * Asc * (NA_cracked - c)^2 + n * As * (d - NA_cracked)^2"),
    "Neutral Axis Depth at failure (x_ult)": (f"{x_ult:.3f} mm", "(As - Asc) * fyd / (0.8 * fcd * b)"),
    "Moment of Resistance M_rd": (M_rd, "M_rd = As * fyd * (d - 0.4 * x)"),
    # "Moment of Resistance M_rd2": (M_rd2, "M_rd2 = (fcd * 0.8 * x * b * (d - 0.4 * x) + fyd * Asc * (d - c)) * 1e-6"),
    "Moment of First Crack (M_cr)": (M_cr, "M_cr = (f_ctm * I_uncr) / (h - x)"),
}

print("--- Results ---")
for key, value in results.items():
    print(f"{key}: {value[0]}")
    
ρ = As / (b * d)  # Reinforcement ratio
ρ_cr = Asc / (b * d)  # Compression reinforcement ratio

k = ((((ρ+ρ_cr)**2 * n**2) + (2*n*(ρ + ρ_cr*(c/d))))** 0.5) - ((ρ + ρ_cr) * n) # Neutral axis depth ratio
print("neutral axis depth (mm):", k * d)
print("neutral axis depth (inches):", (k * d) / 25.4)

moment = 100  # kN·m

from sympy import symbols, Eq, solve
import pandas as pd
fc = symbols('fc')
fsc = ((k*d - c) / (k * d)) * (n*fc)
fs = ((1-k)/k) *n*fc
eq = Eq(0.5 * fc * b * k * d * (d - (k*d/3)) + (fsc * Asc * (d - c)), moment*1e6)
sol = solve(eq, fc)
print("fc:", sol[0], "MPa")
print("fs:", fs.subs(fc, sol[0]), "MPa")
print("fsc:", fsc.subs(fc, sol[0]), "MPa")

# Generate a range of moments from 0 to M_cr
moments = np.linspace(0, M_cr, 100)
fc_values = []

# Calculate fc for each moment
for moment in moments:
    eq = Eq(0.5 * fc * b * k * d * (d - (k * d / 3)) + (fsc * Asc * (d - c)), moment * 1e6)
    sol = solve(eq, fc)
    if sol:
        fc_values.append(float(sol[0]))
    else:
        fc_values.append(0)

        # Create a DataFrame with moments and fc_values
        data = {'Moment (kNm)': moments, 'fc (MPa)': fc_values}
        df = pd.DataFrame(data)
        
        # Display the DataFrame
        print(df)
# # Plot Moment vs fc with annotated points and curve
# plt.figure(figsize=(8, 6))
# plt.plot(moments, fc_values, label="Moment vs fc", color='green')  # Plot the curve
# plt.scatter(moments[::10], [fc_values[i] for i in range(0, len(fc_values), 10)], color='red', s=10, label="Annotated Points")  # Plot only annotated points

# # Annotate every 10th point
# for i in range(0, len(moments), 10):
#     plt.annotate(f"({moments[i]:.1f}, {fc_values[i]:.2f})", (moments[i], fc_values[i]), textcoords="offset points", xytext=(5, 5), fontsize=8)
#     # Annotate the last point
#     plt.scatter(moments[-1], fc_values[-1], color='red', s=10)  # Add red marker for the last point
#     plt.annotate(f"({moments[-1]:.1f}, {fc_values[-1]:.2f})", (moments[-1], fc_values[-1]), textcoords="offset points", xytext=(-50, -10), fontsize=8)

# plt.xlabel("Moment (kNm)")
# plt.ylabel("fc (MPa)")
# plt.title("Moment vs fc")
# plt.grid(True)
# plt.legend()
# plt.show()
