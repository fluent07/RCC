import math as m
import logging
# import ace_tools as tools

def newtonR(f, x0):
    tolf = 1e-08  # Tolerance on the function value
    tolx = 1e-08  # Tolerance on x-value change
    dx = 1e-08
    df = lambda x: (f(x + dx) - f(x)) / dx
    iter_root = [x0]
    max_iterations = 1000
    
    for k in range(1, max_iterations):
        try:
            iter_root.append((iter_root[k - 1]) - (f(iter_root[k - 1]) / df(iter_root[k - 1])))
            if abs(f(iter_root[k])) <= tolf or abs(iter_root[k] - iter_root[k - 1]) <= tolx:
                return iter_root[k]
        except ZeroDivisionError:
            logging.error("Derivative became zero; method failed to converge.")
            return None
    
    logging.error("Newton-Raphson method did not converge after max iterations.")
    return None

# Given data
b = 800 # mm, width of section
h = 300 # mm, total height
c = 40  # mm, cover from top and bottom
d = h - c  # Effective depth
n = 15  # Modular ratio

def area(diameter):
    return (m.pi / 4) * diameter**2

# Reinforcement details
Asc = 2 * area(14)  # Compression reinforcement area (mm^2)
As = 2 * area(20)   # Tension reinforcement area (mm^2)

# Material properties
f_ck = 25  # MPa, characteristic compressive strength of concrete
f_y = 450  # MPa, yield strength of steel
gamma_c = 1.5  # Safety factor for concrete
gamma_s = 1.15  # Safety factor for steel
alpha_cc = 0.85  # Concrete strength reduction factor

# Design strengths
fcd = alpha_cc * (f_ck / gamma_c)  # MPa (factored concrete compressive strength)
fyd = f_y / gamma_s  # MPa (factored steel yield strength)

# Neutral axis depth (x) from force equilibrium - compression and tension
x = (As - Asc) * fyd / (0.8 * fcd * b)

# Design moment resistance (Mrd)
M_rd = As * fyd * (d - 0.4 * x) / (10**6)  # Convert to kNm
M_rd2 = (fcd * 0.8 * x * b * (d - 0.4 * x) + fyd * Asc * (d - c)) * 1e-6

# Neutral axis for uncracked section
Eqn_NA_Uncracked = lambda x: ((b*x**2)/2) + (n*Asc*(x-c)) - ((b*(h-x)**2)/2) - (n*As*(d-x))
NA_uncracked = newtonR(Eqn_NA_Uncracked, 100)

I_uncr = (b/3) * NA_uncracked**3 + n * Asc * (NA_uncracked - c)**2 + (b/3) * (h - NA_uncracked)**3 + n * As * (d - NA_uncracked)**2

# Neutral axis for cracked section
Eqn_NA_cracked = lambda x: (b*x**2/2) + (n*Asc*(x-c)) - (n*As*(d-x))
NA_cracked = newtonR(Eqn_NA_cracked, 100)
I_cr = (b/3) * NA_cracked**3 + n * Asc * (NA_cracked - c)**2 + n * As * (d - NA_cracked)**2

# First moment of cracking (M_cr)
f_ctm = 0.3 * (f_ck ** (2/3))  # MPa, mean tensile strength of concrete
M_cr = (f_ctm * I_uncr) / (h - NA_uncracked) / (10**6)

# Removing compression reinforcement
x_no_compression = (As * fyd) / (0.8 * fcd * b)
Eqn_NA_Uncracked_no_comp = lambda x: ((b*x**2)/2) - ((b*(h-x)**2)/2) - (n*As*(d-x))
NA_uncracked_no_comp = newtonR(Eqn_NA_Uncracked_no_comp, 100)
Eqn_NA_cracked_no_comp = lambda x: (b*x**2/2) - (n*As*(d-x))
NA_cracked_no_comp = newtonR(Eqn_NA_cracked_no_comp, 100)

# Checking conditions without compression reinforcement
epsilon_s_no_comp = (fyd / 200000) * ((d - x_no_compression) / x_no_compression)
sigma_c_no_comp = M_rd / (x_no_compression * b)
sigma_c_limit_no_comp = 0.6 * fcd
needs_compression_reinf_no_comp = epsilon_s_no_comp < 2.5e-3 or sigma_c_no_comp > sigma_c_limit_no_comp

# Store results
data = {
    "Neutral Axis (Uncracked) (mm)": NA_uncracked,
    "Moment of Inertia (Uncracked) (mm^4)": I_uncr,
    "Neutral Axis (Cracked) (mm)": NA_cracked,
    "Moment of Inertia (Cracked) (mm^4)": I_cr,
    "Moment of Resistance M_rd (kNm)": M_rd,
    "Moment of Resistance M_rd2 (kNm)": M_rd2,
    "Moment of First Crack (M_cr) (kNm)": M_cr,
    "Ultimate Neutral Axis Depth (x_ult) Without Compression (mm)": x_no_compression,
    "Steel Strain (ε_s) Without Compression": epsilon_s_no_comp,
    "Concrete Stress (MPa) Without Compression": sigma_c_no_comp,
    "Concrete Stress Limit (MPa)": sigma_c_limit_no_comp,
    "Needs Compression Reinforcement?": needs_compression_reinf_no_comp,
}


# Import colorama for cross-platform color support
from colorama import Fore, Style

# Define colors
colors = {
    "Neutral Axis (Uncracked)": Fore.CYAN,
    "Moment of Inertia (Uncracked)": Fore.GREEN,
    "Neutral Axis (Cracked)": Fore.CYAN,
    "Moment of Inertia (Cracked)": Fore.GREEN,
    "Moment of Resistance M_rd": Fore.YELLOW,
    "Moment of Resistance M_rd2": Fore.YELLOW,
    "Moment of First Crack (M_cr)": Fore.RED,
    "Ultimate Neutral Axis Depth (x_ult)": Fore.MAGENTA,
}

# Define ANSI color code for cyan (key) and reset code
CYAN = Fore.GREEN
RESET = "\033[0m"

# Print dictionary with colored keys
for key, value in data.items():
    print(f"{CYAN}{key}:{RESET} {value}")

print("\n\n")

