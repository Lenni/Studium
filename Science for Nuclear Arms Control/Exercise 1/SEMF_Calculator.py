import numpy as np

################ DEFINE CONSTANTS ##############
a_v = 15.8
a_s = 18.3
a_C = 0.714
a_A = 23.2
a_p = 12.0
###############################################


print("Please input the Z and A numbers for the nucleus")

A = int(input("A:"))
Z = int(input("Z:"))

if A < Z:
    print("A has to be greater than Z")
    exit(0)

delta = 0

if A % 2 == 0:
    if Z % 2 == 0:
        delta = a_p * pow(A, -1.0/2.0)
    else:
        delta = -a_p * pow(A, -1.0/2.0)


E_B = a_v*A - a_s*pow(A, 2.0/3.0) - a_C*(Z*(Z-1))/pow(A, 1.0/3.0) - a_A*pow(A-2*Z, 2)/A + delta

print("{:.3}".format(E_B))