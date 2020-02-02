import matplotlib.pyplot as plt 
import numpy as np 

eka = 1
toka = 2
kolkki = 3

aika = []
x1_akseli = []
y1_akseli = []
z1_akseli = []
x2_akseli = []
y2_akseli = []
z2_akseli = []
x3_akseli = []
y3_akseli = []
z3_akseli = []


with open("testi1.dat", "r") as f:
    d = f.readlines()
    for i in d:
        k = i.split(",")
#print(k)

        aika.append(float(k[0]))
        x1_akseli.append(float(k[eka]))
        y1_akseli.append(float(k[toka]))
        z1_akseli.append(float(k[kolkki]))
"""
with open("testi2.dat", "r") as f:
    d = f.readlines()
    for i in d:
        k = i.split(",")
#print(k)
        x2_akseli.append(float(k[eka]))
        y2_akseli.append(float(k[toka]))
        z2_akseli.append(float(k[kolkki]))

with open("testiakseli.dat", "r") as f:
    d = f.readlines()
    for i in d:
        k = i.split(",")
#print(k)
        x3_akseli.append(float(k[eka]))
        y3_akseli.append(float(k[toka]))
        z3_akseli.append(float(k[kolkki]))
"""
#for i in range(len(aika)):
#		print(aika[i])
#		print(x_akseli[i])		
plt.title("Kuvaaja")
plt.xlabel("Aika")
plt.ylabel("Kiihtyvyys")
plt.plot(aika, x1_akseli, "blue")		#SININEN
plt.plot(aika, y1_akseli, "grey")		#ORANSSI
plt.plot(aika, z1_akseli, "black")		#VIHREÄ

#plt.plot(aika, x2_akseli, "red")
#plt.plot(aika, y2_akseli, "purple")
#plt.plot(aika, z2_akseli, "green")
#plt.plot(akseli1, akseli2)

#plt.plot(aika, x3_akseli, "blue")
#plt.plot(aika, y3_akseli)
#plt.plot(aika, z3_akseli, "black")
plt.show()