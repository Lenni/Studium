#! /usr/bin/env python3
"""
Read the SERPENT results file.

@author: Benjamin Jung
"""

def get_multiplication_factor(filepath):
    """Read the multiplication factor data

    Parse the result file produced by serpent and add
    the multiplication factor data to a dictionary.

    Patameters
    ----------
    filepath:   filepath of the result (_res.m) file
                produced by SERPENT

    Output
    ------
    keff:       dictionary of two different estimators
                k_eff for the multiplication factor.
                It is sufficient to use either estimator
                for the exercises.
    """

    keff = []
    results = open(filepath, 'r')
    for f in results:
        if len(f.split()) < 2:
            pass
        elif f.split()[0] == "ANA_KEFF":
            keff.append(float(f.split()[-7]))

    return keff

