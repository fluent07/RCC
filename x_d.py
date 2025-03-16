import numpy as np
import sympy as sp
d = sp.symbols('d')
# fyk = 260
rck = np.empty(0)
rck = np.append(rck,25)
rck = np.append(rck,30)
rck = np.append(rck,37)
rck = np.append(rck,45)
rck = np.append(rck,60)
x = np.empty(0)
z = np.empty(0)
n = 15
sigma_s = 260

i = 0
while(i<len(rck)):
    sigma_c = rck[i]/3
    # x = np.append(x, lambda d:(sigma_c/(sigma_s/n+sigma_c)*d))
    x = np.append(x,(sigma_c/(sigma_s/n+sigma_c)*d))
    # z = np.append(z, lambda d: d-x[i]/3)
    z = np.append(z, d-x[i]/3)
    print("For Rck",rck[i], ", x is",x[i],", z is",z[i])
    i+= 1

