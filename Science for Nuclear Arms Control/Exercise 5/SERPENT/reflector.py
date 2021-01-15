import numpy as np
from os import system
import matplotlib.pyplot as plt
import sys

SERPENT_Template = """
mat fuel -19.8  94239.09c -100 rgb 50 200 10
mat ref -1.85   4009.09c -100 rgb 75 75 75

surf Sphere  sph 0 0 0 {diameter}
surf reflector sph 0 0 0 {diameter_2}

surf box cube 0 0 0 {box_size}

cell Core 0 fuel -Sphere
cell shell 0 ref -reflector Sphere
cell Box 0 void  reflector Sphere -box

cell Out 0 outside box

set bc 1
set pop 10000 100 50


set tpa 0 0.1 1 100 200

plot 13 1000 1000"""

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


def run_serpent(filepath, options=None, **kwargs):
    ###
    # @params filepaths
    # @return result file name
    ###

    if options is None:
        options = {}

    opt_str = " "

    for key in options:
        opt_str += "-{key} {param} ".format(key=key, param=options[key])

    system("source ./init.sh && sss2 {options} {file}".format(options=opt_str, file=filepath))

    return "{filename}_res.m".format(filename=filepath)


def generate_file(filepath, **params):
    template = SERPENT_Template.format(**params)

    with open(filepath, "w") as serpent_file:
        serpent_file.write(template)
        serpent_file.close()


if __name__ == "__main__":

    bins = 0

    if len(sys.argv) > 2:
        bins = int(sys.argv[1])
        limit = int(sys.argv[2])
    else:
        bins = 4
        limit = 10

    thicknesses = np.linspace(0, limit, bins)
    sphere_diameter = np.power(4000.0/(4.0/3.0*np.pi*19.8), 1.0/3.0)
    filenames = []

    for distance in thicknesses:

        parameters = {"diameter": str(sphere_diameter),
                      "diameter_2": str(sphere_diameter+distance),
                      "box_size": 2 * sphere_diameter +  distance}

        filename = "reflector_{distance:.3f}".format(distance=distance)
        filenames.append(filename)

        generate_file(filename, **parameters)

    results = []

    for file in filenames:
        results.append(run_serpent(file, options={"omp": 100}))

    print(results)
    k_effs = []

    for result in results:
        k_effs.append(get_multiplication_factor(result))

    figure = plt.figure(figsize=(16, 9))

    plt.plot(thicknesses, k_effs, marker="o", color="r", label="Simulated k_eff")
    plt.legend()

    plt.xlabel("Reflector thickness in cm")
    plt.ylabel("Neutron multiplication factor")

    plt.savefig("criticality_reflector.png", bbox_inches="tight", dpi=900)