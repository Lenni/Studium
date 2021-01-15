#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import division,print_function,absolute_import,unicode_literals

import numpy as np
from scipy import sparse

'''spinop module
generates matrix representations for spin operators

spins on sites 1,2,...,Ns

Usage:
    import spinop
    Ns = 4 # number of spins
    H = sparse.csr_matrix((2**Ns,2**Ns),dtype=np.complex128)
    # define Hamiltonian terms, e.g., for a bond between spins i and j for the z component
    H += -J * spinop.Sz(i,N=Ns).dot(spinop.Sz(j,N=Ns))
    H += ...

Links:
https://docs.scipy.org/doc/numpy/reference/generated/numpy.linalg.eigh.html
https://docs.scipy.org/doc/scipy/reference/sparse.html
'''

# 2x2 sparse Pauli matrices and S+ / S- / identity
# show via spinop.Sm2.toarray()
Sp2 = sparse.csr_matrix([[0,1],[0,0]]) 
Sm2 = sparse.csr_matrix([[0,0],[1,0]])
Sx2 = 0.5*(Sp2+Sm2)
Sy2 = -0.5j*(Sp2-Sm2)
Sz2 = 0.5*sparse.csr_matrix([[1,0],[0,-1]]) # states UP | DOWN
Id2 = sparse.identity(2)

def sparse_op(op2,pos,N):
    '''local arbitrary spin operator to full Hilbert space representation'''
    return sparse.kron(sparse.kron(sparse.identity(2**(pos-1)),op2),sparse.identity(2**(N-pos)))

def Sp(pos,N=2):
    '''returns S^+ operator on spin idx=1,2,3,4,...Ns in full Hilbert space of Sz basis of all spins - but sparse'''
    return sparse_op(Sp2,pos,N)

def Sm(pos,N=2):
    '''returns S^- operator on spin idx=1,2,3,4,...Ns in full Hilbert space of Sz basis of all spins - but sparse'''
    return sparse_op(Sm2,pos,N)

def Sx(pos,N=2):
    '''returns S^x operator on spin idx=1,2,3,4,...Ns in full Hilbert space of Sx basis of all spins - but sparse'''
    return sparse_op(Sx2,pos,N)

def Sy(pos,N=2):
    '''returns S^y operator on spin idx=1,2,3,4,...Ns in full Hilbert space of Sy basis of all spins - but sparse'''
    return sparse_op(Sy2,pos,N)

def Sz(pos,N=2):
    '''returns S^z operator on spin idx=1,2,3,4,...Ns in full Hilbert space of Sz basis of all spins - but sparse'''
    return sparse_op(Sz2,pos,N)

if __name__ == '__main__':
    print("use as library via 'import spinop'")


