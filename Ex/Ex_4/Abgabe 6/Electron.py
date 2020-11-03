#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
from mendeleev import element


l_dict = {"s": 0,
          "p": 1,
          "d": 2,
          "f": 3,
          "g": 4,
          "h": 5,
          "i": 6}

inv_l_dict = {v: k for k, v in l_dict.items()}


def generate_basestate(max_n, max_l, max_e):
    
    result = ""
    
    kaestchen = max_n*2
    
    n = 0
    l = 0
    
    for k in range(kaestchen):
        elements = math.ceil(k/2)-1
        for element in range(elements, -1, -1):
            n = k - element
            l = element
            e = 4*l+2
            if n == max_n and l == max_l:
                #e = max_e
                #orbital = "{}{}{} ".format(n, inv_l_dict[l], e)
                #result += orbital
                break
            else:
                orbital = "{}{}{} ".format(n, inv_l_dict[l], e)
                result += orbital
        else:
            continue
        break
        
    return result

def generate_groundstate(z):
    
    result = ""
    
    kaestchen = z+1
    
    n = 0
    l = 0
    
    sum_e = 0
    
    for k in range(kaestchen):
        elements = math.ceil(k/2)-1
        for element in range(elements, -1, -1):
            n = k - element
            l = element
            e = 4*l+2
            
            
            sum_e += e
            
            if sum_e >= z:
                e = e-(sum_e - z)
                orbital = "{}{}{} ".format(n, inv_l_dict[l], e)
                result += orbital
                break
            else:
                orbital = "{}{}{} ".format(n, inv_l_dict[l], e)
                result += orbital
        else:
            continue
        break
        
    return result

def parse_input(in_string):
    
    print("|  n  |  l  | Electrons |")
    print("-------------------------")
    
    valid = True

    sum_elek = 0
    conf_set = False
    i = 0
    
    while i < len(in_string):
        n = int(in_string[i])
        i +=1
        l = in_string[i]
        i +=1
        
        l_p = l_dict[l]
        
        e = ""
        
        while i < len(in_string):
            x = in_string[i]
            i += 1
            if x == " ":
                break
            else:
                e += x
        elek = int(e)
        
        if not conf_set:
            highest_config = (n, l_p, elek)
            conf_set = True
        
        sum_elek += elek
        
        
        print("|{:^5}|{:^5}|{:^11}|".format(n, inv_l_dict[l_p], elek))
        
        if(n < l_p):
            valid = False
            print("Orbital Quantum Number greater than Principal Quantum Number")
            break
    
        if(elek > (4*l_p + 2)):
            valid = False
            print("Number of Electrons too large for Orbital")
            break
    return (valid, sum_elek, highest_config)
        

inp = input("Elektronenkonfiguration: ")


valid, sum_e, highest = parse_input(inp)
    
print("")
print("")
base = generate_basestate(highest[0], highest[1], highest[2])

_, sum_e, _ = parse_input(base + inp)
    

if valid:
    print("Configuration is valid!")
    
    element_name = element(sum_e).name
    
    ground = generate_groundstate(sum_e)
    
    print(element_name)
    print("")
    
    print(base + inp)
    print(ground)
    
    if((base + inp) == ground[:-1]):
        print("Element is in lowest Energy State")
    else:
        print("Element is in excited State")
