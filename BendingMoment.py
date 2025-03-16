import numpy as np
import sympy as s
import matplotlib.pyplot as plt

force = 2
# f2 = 5
l= 5

dx = 0.1

x = np.empty(0)
x = np.append(x,0)
m = np.empty(0)
m2 = np.empty(0)
# m = np.append(m,force*x[0])

i = 0
while min(x)>(-l+dx):
    x = np.append(x,x[i]-dx)
    # m = np.append(m, force*x[i])    
    i = i+1

i=0
while i<len(x+dx):
    m = np.append(m,force*x[i])
    i += 1

i=0
while i<len(x+dx):
    m2 = np.append(m2,force*x[i]*x[i]/2)
    i += 1

y = np.zeros(len(x))
print(m,m2)
print(x)
# plt.ylim(0,-30)
plt.plot(x,y,color='k')
#shear force plot
plt.plot(x,-(y+force),color='b')
p=0.01
while p<0.4:
    plt.plot(x,y+p,color='k')
    p = p+0.01
plt.plot(x,p+abs(m), color = 'r')
plt.plot(x, p+m2, color = 'g')
plt.gca().invert_yaxis()
plt.show()






