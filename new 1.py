import test as cn
import math as m

def area(d):
    return((m.pi/4)*d**2)
   
b = 1200
h = 400
c = 40
d = h-c
Asc = 6*area(14)
As = 6*area(14)+4*area(20)
print(Asc,As)
n = 15

fck = 25
fyk = 450
fcd = 0.85/1.5*fck
fyd = fyk/1.15
Es = 210000
ecu = 0.0035
esy = fyd/Es
# moment = 257.8*1000*1000
ps = As/b/d
psc = Asc/b/d
print("\nReinforcement ratio:",(ps-psc)*100)
print("Ps",ps*100)
print('Psc',psc*100)

#At SLS
print("\nAT SLS")
Eqn_NA_cracked = lambda x: (b*x**2)/2+(n*Asc*(x-c))-(n*As*(d-x))
NA_cracked = cn.newtonR(Eqn_NA_cracked,100)
print("Cracked neutral axis",NA_cracked)
I_cracked = (b*NA_cracked**3)/3+(n*Asc*(NA_cracked-c)**2)+(n*As*(d-NA_cracked)**2)
print("MOI",I_cracked)
# sigma_c = moment*NA_cracked/I_cracked
# print("Stress in concrete at SLS", sigma_c)
# sigma_s = n*moment*(d-NA_cracked)/I_cracked
# print("Stress in Tension Steel at SLS", sigma_s)
# sigma_sc = n*moment*(NA_cracked-c)/I_cracked
# print("Stress in Compression Steel at SLS", sigma_sc)
#AT ULS
print("\nAT ULS")
NA_ULS = (fyd*(As-Asc))/(0.8*b*fcd)
NA_ULS1 = (ps-psc)*d*fyd/fcd/0.8
# print("NA21:",NA_ULS1/10)
print("NA",NA_ULS)
esc = ecu/NA_ULS*(NA_ULS-c)
print("Strain in Compression Steel:",esc)
if esc<esy:
    print("es'< esy")
    Eqn_NA_cracked3 = lambda x: (0.8*b*x*fcd)+(Asc*Es*ecu*(x-c)/x)-(As*fyd)
    NA_ULS = cn.newtonR(Eqn_NA_cracked3,100)
    print("NA3",NA_ULS)
    esc = ecu/NA_ULS*(NA_ULS-c)
    print(esc)
else:
    print("es'> es")
Mrd = 0.8*b*NA_ULS*fcd*(d-0.4*NA_ULS)+(Asc*Es*ecu*(NA_ULS-c)/NA_ULS)*(d-c)
print("Mrd:", Mrd/1000000)
Mrd_T = As*fyd*(d-0.4*NA_ULS)
Mrd_T2 = As*fyd*(0.9*d)
delta = 0.44+1.25*(0.6+0.0014/ecu)*NA_ULS/d
# print("Mrd2:", Mrd_T/1000000)
# print("Mrd2:", Mrd_T2/1000000)
print("xu/d:",round(NA_ULS/d,3))
print("delta:",round(delta,3),"\n")
# NA_cracked = cn.newtonR(Eqn_NA_cracked,100)
# I_cracked = (b*NA_cracked**3)/3+(n*Asc*(NA_cracked-c)**2)+(n*As*(d-NA_cracked)**2)
# I_cracked2 = (b*NA_ULS**3)/3+(n*Asc*(NA_ULS-c)**2)+(n*As*(d-NA_ULS)**2)
# print("cracked section:")
# print("NA:",NA_cracked,"mm")
# print("NA2:",NA_ULS,"mm")
# print("I_cracked:",I_cracked/10000,"cm4")
# print("I_cracked2:",I_cracked2/10000,"cm4")
# # print("I_uncracked2/I_cracked2",I_uncracked2/I_cracked2,"\n")

#Crack Spacing
Med_characteristic = 169.2*1000*1000
Med_frequent = 146.9*1000*1000
Med_quasipermanent = 143.5*1000*1000
fctm = 0.3*fck**(2/3)
hc_eff = min(h/2,(h-NA_cracked)/3,2.5*(h-d))
Ac_eff =hc_eff*b
Ps_eff = As/Ac_eff
alpha_e = 6.1
Class = 'XC4'
ordinarie = ['X0','XC1','XC2','XC3','XF1']
aggressive = ['XC4','XD1','XS2','XA1','XA2','XF2','XF3']
molto_aggressive = ['XD2','XD3','XS2','XS3','XA3','XF4']
# print(len(ordinarie))
# i = 0
# flag  = 0
# while flag==0:
#     while(i<len(ordinarie)):
#         if Class==ordinarie[i]:
#             i = i+1 
#             print("for Poco Sensibile,frequente w<=w3, quasi permanente w<=w2")
#             flag = 1
#     while(i<len(aggressive)):
#         if Class==aggressive[i]:
#             i = i+1 
#             print("for Poco Sensibile,frequente w<=w2, quasi permanente w<=w1")
#             flag = 1
#     while(i<len(molto_aggressive)):       
#         if Class==molto_aggressive[i]:
#             i = i+1 
#             print("for Poco Sensibile,frequente w<=w1, quasi permanente w<=w1") 
#             flag = 1

    

w1 = 0.2
w2 = 0.3
w3 = 0.4

kt = 0.6
k1 = 0.8
k2 = 0.5
k3 = 3.4
k4 = 0.425
#Verifications at SLS
sigmaC_limit_characteristic = 0.6*fck
sigmaC_limit_quasipermanent = 0.45*fck
sigmaS_limit_characteristic = 0.8*fyk

sigmaC_characteristic = Med_characteristic/I_cracked*NA_cracked
sigmaC_quasipermanent = Med_quasipermanent/I_cracked*NA_cracked
sigmaS_characteristic = n*Med_characteristic/I_cracked*(d-NA_cracked)
sigmaS_quasipermanent = n*Med_quasipermanent/I_cracked*(d-NA_cracked)
sigmaS_frequent = n*Med_frequent/I_cracked*(d-NA_cracked)

if sigmaC_characteristic<=sigmaC_limit_characteristic:
    print("Stress of concrete in characteristic=",sigmaC_characteristic,"<",sigmaC_limit_characteristic)
if sigmaC_quasipermanent<=sigmaC_limit_quasipermanent:
    print("Stress of concrete in Quasi-permanent=",sigmaC_quasipermanent,"<",sigmaC_limit_quasipermanent)
if sigmaS_characteristic<=sigmaS_limit_characteristic:
    print("Stress of Steel in Characteristic=",sigmaS_characteristic)

#for frequent w2<=0.3mm
esm = (sigmaS_frequent-kt*fctm*(1+alpha_e*Ps_eff)/Ps_eff)/Es
delta_sm = (k3*c+k1*k2*k4*20/Ps_eff)/1.7
wk = 1.7*esm*delta_sm
print("Crack width w_f=",wk)
#for frequent w1<=0.2mm
esm = (sigmaS_quasipermanent-kt*fctm*(1+alpha_e*Ps_eff)/Ps_eff)/Es
delta_sm = (k3*c+k1*k2*k4*20/Ps_eff)/1.7
wk = 1.7*esm*delta_sm
print("Crack width w_qp=",wk)