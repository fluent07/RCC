import test as cn
import math as m

def area(d):
    return((m.pi/4)*d**2)
   
b = 300
h = 450
c = 40
d = h-c
Asc = 2*area(14)
As = 4*area(20)
n = 15

fck = 30
fyk = 450
fcd = 0.85/1.5*fck
fyd = fyk/1.15
Es = 210000
ecu = 0.0035
esy = fyd/Es
# n1 = fyd / (0.3 * fck)
# print(n1)
Eqn_NA_Uncracked = lambda x: ((b*x**2)/2)+(n*Asc*(x-c))-((b*(h-x)**2)/2)-(n*As*(d-x))
NA_uncracked = cn.newtonR(Eqn_NA_Uncracked,100)
print("NA:",NA_uncracked,"mm")
I_uncracked = (b/3)*NA_uncracked**3 + n*Asc*(NA_uncracked-c)**2 + (b/3)*(h-NA_uncracked)**3 + n*As*(d-NA_uncracked)**2 #(b*h**3)/3+(n*Asc*(NA_uncracked-c)**2)+(n*As*(d-NA_uncracked)**2)+b*h*(h/2-NA_uncracked)**2
print("I_uncracked:",I_uncracked/10000,"cm4")
Eqn_NA_Uncracked2 = lambda x: ((b*x**2)/2)+((n-1)*Asc*(x-c))-((b*(h-x)**2)/2)-((n-1)*As*(d-x))
NA_uncracked2 = cn.newtonR(Eqn_NA_Uncracked2,100)
print("\nuncracked section:")
print("NA2:",NA_uncracked2,"mm")
I_uncracked2 = (b*NA_uncracked2**3)/3+(b*(h-NA_uncracked2)**3)/3+((n-1)*Asc*(NA_uncracked2-c)**2)+((n-1)*As*(d-NA_uncracked2)**2)
print("I_uncracked2:",I_uncracked2/10000,"cm4")

# NA_uncracked_test = 358
# I_uncracked_test = (b*NA_uncracked_test**3)/3+(b*(h-NA_uncracked_test)**3)/3+((n-1)*Asc*(NA_uncracked_test-c)**2)+((n-1)*As*(d-NA_uncracked_test)**2)
# print("I_uncracked_test:",I_uncracked_test,"mm4\n")

Eqn_NA_cracked = lambda x: (b*x**2)/2+(n*Asc*(x-c))-(n*As*(d-x))
NA_cracked = cn.newtonR(Eqn_NA_cracked,100)
I_cracked = (b*NA_cracked**3)/3+(n*Asc*(NA_cracked-c)**2)+(n*As*(d-NA_cracked)**2)
print("\ncracked section:")
print("NA:",NA_cracked,"mm")
print("I_cracked:",I_cracked/10000,"cm4\n")

NA_cracked_u = (fyd*(As-Asc))/(0.8*b*fcd)
esc = ecu/NA_cracked_u*(NA_cracked_u-c)
print("NA2:",NA_cracked_u,"mm")
print("esc",esc,esy)
if esc<esy:
    print('true')
    Eqn_NA_cracked3 = lambda x: (0.8*b*x*fcd)+(Asc*Es*ecu*(x-c)/x)-(As*fyd)
    NA_cracked2 = cn.newtonR(Eqn_NA_cracked3,100)
    print("NA3",NA_cracked2/10)
    I_cracked_u = (b*NA_cracked2**3)/3+(n*Asc*(NA_cracked2-c)**2)+(n*As*(d-NA_cracked2)**2)
    print("I_cracked_u:",I_cracked_u/10000,"cm4")
    print("I_uncracked/I_cracked",I_uncracked/I_cracked,"\n")
    Mrd = 0.8*fcd*NA_cracked2*b*(d-0.4*NA_cracked2)