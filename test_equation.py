# program to get line equation
# program to plot line equation
import matplotlib.pyplot as plt
import sympy as smp

# m = -0.5
# c = 12.5
# y = lambda x: m*x+c
# x = 25
# while x>=0:
#     print("(",x,",",y(x),")")
#     x = round(x-0.1,2)
x, y = smp.symbols("x y", real=True)

A = [1, -5]
B = [-6, -6]
x1 = A[0]
y1 = A[1]
x2 = B[0]
y2 = B[1]
# print(x1,y1)
# print(x2,y2)
Y_points = []
X_points = []
# y = lambda x: ((y2 - y1) / (x2 - x1)) * (x - x1) + y1
e = ((y2 - y1) / (x2 - x1)) * (x - x1) + y1
c = (y2 - y1) / (x2 - x1)*(-x1)+y1
m = (e-c)/x
y = m*x+c
# equation = smp.Eq(y, e)
# # y_abs = m * xs + c
# solution = smp.solve(equation, y)
# # print(solution)
# # print(y, m_abs)
# m = solution[0].as_coefficients_dict()[x]
# c = solution[0].as_coefficients_dict()[1]
print(m,c)
# print(f"The slope 'm' is: {m}")
# print(f"The y-intercept 'c' is: {c}")
# print(f"m = {sol[m]}")
# print(f"c = {sol[c]}")
if m<1:
    limit = 20
else:
    limit = 5
it = limit
while it >= -limit:
    X_points.append(it)
    Y_points.append(e.subs(x, it))
    it -= 1
# # print("x=", x, "y=", y(x))
# print(X_points, "\n", Y_points)
# # plt.figure(1)
plt.plot(X_points, Y_points)
# for i in range(-50, 50, 1):
#     plt.plot(0, i)
#     plt.plot(i, 0)
# plt.grid(True, "both")
plt.axhline(y=0, color="k")
plt.axvline(x=0, color="k")
plt.show()


# x = 10
# for i in range(10):
#     y = lambda x: 2*x
#     print(x,y(x)) #y(x)
#     x-=1

# Import sympy and define symbols
# import sympy as sp

# x, y = sp.symbols("x y")

# # Create an equation object
# eq = sp.Eq(y, 1.25 * x + 0.2)

# # Solve the equation for m and c
# sol = sp.solve(eq, (m, c))

# # Print the values of m and c
# print(f"m = {sol[m]}")
# print(f"c = {sol[c]}")
