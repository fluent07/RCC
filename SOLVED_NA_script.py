from logging import error
import math as m

print("\n\n")
# Given data
b = 300  # mm, width of section
h = 450  # mm, total height
c = 40  # mm, cover from top and bottom to the centre of the reinforcement
d = h - c
n = 15

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

def area(d):
    return (m.pi / 4) * d**2

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
        iter_root.append(
            (iter_root[k - 1]) - (f(iter_root[k - 1]) / df(iter_root[k - 1]))
        )
        # find the value of xk that makes the tangent to the function f = 0 at a certain step k
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


# Reinforcement details
Asc = 2 * area(14)  # Compression reinforcement area (mm^2)
As = 4 * area(20)  # Tension reinforcement area (mm^2)


# Material properties
f_ck = 25  # MPa, characteristic compressive strength of concrete
f_y = 450  # MPa, yield strength of steel
gamma_c = 1.5  # Safety factor for concrete
gamma_s = 1.15  # Safety factor for steel
alpha_cc = 0.85  # Concrete strength reduction factor
Es = 210000 # Young's modulous of steel

# Design strengths
fcd = alpha_cc * (f_ck / gamma_c)  # MPa
fyd = f_y / gamma_s  # MPa
results = {}

def check_for_compression_reinforcement():
    # Check need for compression reinforcement
    x_no_Asc = (As * fyd) / (0.8 * fcd * b)

    # Calculate neutral axis for uncracked section - no compressive reinf
    Eqn_NA_Uncracked_no_Asc = (
        lambda x: ((b * x**2) / 2) - ((b * (h - x) ** 2) / 2) - (n * As * (d - x))
    )
    NA_uncracked_no_Asc = newtonR(Eqn_NA_Uncracked_no_Asc, 100)

    # Calculate neutral axis for cracked section - no compressive reinf
    Eqn_NA_cracked_no_comp = lambda x: (b * x**2 / 2) - (n * As * (d - x))
    NA_cracked_no_Asc = newtonR(Eqn_NA_cracked_no_comp, 100)
    
    # Design moment resistance (Mrd)
    M_rd = As * fyd * (d - 0.4 * x_no_Asc) / (10**6)  # Convert to kNm
    M_rd2 = fcd * 0.8 * x_no_Asc * b * (d - 0.4 * x_no_Asc) * 1e-6
    
    # Recalculate Steel Strain (ε_s) without compression reinforcement
    epsilon_s_no_Asc = (fyd / Es) * ((d - x_no_Asc) / x_no_Asc)

    # Recalculate Concrete Stress (σ_c) without compression reinforcement
    sigma_c_no_Asc = M_rd / (x_no_Asc * b)

    # Check conditions
    x_d_d_ratio_no_Asc = x_no_Asc / d  # Updated neutral axis to depth ratio
    sigma_c_limit_no_Asc = 0.6 * fcd  # Max allowable concrete stress

    # Determine if compression reinforcement is required based on the second and third conditions
    needs_compression_reinf_no_Asc = (
        epsilon_s_no_Asc < 2.5e-3 or sigma_c_no_Asc > sigma_c_limit_no_Asc
    )

    # Store results for checking the second and third conditions
    results = {
        "Neutral Axis (uncracked) mm" : NA_uncracked_no_Asc,
        "Neutral Axis (cracked) mm" : NA_cracked_no_Asc,
        "Ultimate Neutral Axis Depth (x_ult) mm": x_no_Asc,
        "(x_ult) / d  ratio": x_d_d_ratio_no_Asc,
        "Steel Strain (ε_s) Without Compression": epsilon_s_no_Asc,
        "Concrete Stress (MPa) Without Compression": sigma_c_no_Asc,
        "Concrete Stress Limit (MPa)": sigma_c_limit_no_Asc,
        "Needs Compression Reinforcement?": needs_compression_reinf_no_Asc,
    }
    
    # Define ANSI color code for cyan (key) and reset code
    CYAN = Fore.GREEN
    RESET = "\033[0m"

    # Print dictionary with colored keys
    for key, value in results.items():
        print(f"{CYAN}{key}:{RESET} {value}")

    print("\n\n")

check_for_compression_reinforcement()

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

# Cracked moment of inertia (I_cr) - transformed section
Eqn_NA_cracked = lambda x_cr: (b * x_cr**2 / 2) + (n * Asc * (x_cr - c)) - (n * As * (d - x_cr))
NA_cracked = newtonR(Eqn_NA_cracked, 100)
# print("NA_cracked:",NA_cracked,"mm")
# y_n = x / 2  # Neutral axis from top

# Parallel axis theorem to find I_cr
I_cr = (
    (b / 3) * NA_cracked**3
    + n * Asc * (NA_cracked - c) ** 2
    + n * As * (d - NA_cracked) ** 2
)  # (b * x**3) / 3 + (n * As * (d - y_n)**2) + (n * Asc * (y_n - c)**2)

# First moment of cracking (M_cr)
f_ctm = 0.3 * (f_ck ** (2 / 3))  # MPa, mean tensile strength of concrete
y = h / 2  # Distance to extreme fiber

M_cr = (f_ctm * I_uncr) / (h - NA_uncracked) / (10**6)  # Convert to kNm

# Output results
results = {
    "Neutral Axis (Uncracked)": NA_uncracked,
    "Moment of Inertia (Uncracked)": I_uncr,
    "Neutral Axis (Cracked)": NA_cracked,
    "Moment of Inertia (Cracked)": I_cr,
    "Moment of Resistance M_rd": M_rd,
    "Moment of Resistance M_rd2": M_rd2,
    "Moment of First Crack (M_cr)": M_cr,
    "Ultimate Neutral Axis Depth (x_ult)": x_ult / 10,
}


# Define ANSI color code for cyan (key) and reset code
CYAN = Fore.MAGENTA
RESET = "\033[0m"

# Print dictionary with colored keys
for key, value in results.items():
    print(f"{CYAN}{key}:{RESET} {value}")

print("\n\n")
