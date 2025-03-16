import numpy as np
import pandas as pd

# Constants
αcc = 0.85
fck = 20
γc = 1.5
γs = 1.15
fyk = 270

fcd = αcc * (fck/γc)
fyd = fyk/γs

b = 255
d = 460

# Create array of x/d values from 0.15 to 0.65
x_d_values = np.linspace(0.01, 0.65, 300)

# Initialize arrays for results
Mrd_values = []
psb_values = []
As_iter_values = []
lever_arm = []
# Calculate Mrd, ρsb, and As_iter for each x/d value
for x_d_iter in x_d_values:
    ρsb = 0.8 * (x_d_iter) * (fcd/fyd)
    psb_values.append(ρsb*100)
    As_iter = ρsb * b * d
    As_iter_values.append(As_iter)
    x = (fyd/fcd) * (As_iter/(0.8*b))
    Mrd = 0.8 * x * b * fcd * (d - 0.4 * x)
    Mrd_values.append(Mrd/1e6)
    lever_arm.append(d-0.4*x)
    
    if ρsb*100 >= 1.2:
        break

# Create DataFrame
data = {
    "x/d": x_d_values[:len(Mrd_values)],
    "ρsb (%)": psb_values,
    "lever arm": lever_arm,
    "As_iter (mm^2)": As_iter_values,
    "Mrd (kNm)": Mrd_values
}
results_df = pd.DataFrame(data)

# Save to Excel
results_df.to_excel("results.xlsx", index=False)

# import matplotlib.pyplot as plt

# # Plot Mrd vs ρsb
# plt.figure(figsize=(8, 6))
# plt.plot(psb_values, Mrd_values, label="Mrd vs ρsb", color="blue", linewidth=2)

# # Add labels, title, and grid
# plt.xlabel("ρsb (%)", fontsize=12)
# plt.ylabel("Mrd (kNm)", fontsize=12)
# plt.title("Moment Resistance (Mrd) vs Steel Ratio (ρsb)", fontsize=14)
# plt.grid(True, linestyle='--', alpha=0.7)
# plt.legend(fontsize=10)
# plt.tight_layout()

# # Show the plot
# plt.show()
