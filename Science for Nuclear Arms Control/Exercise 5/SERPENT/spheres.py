import numpy as np
from os import system
import matplotlib.pyplot as plt
import sys

SERPENT_Template = """
mat fuel -19.8  94239.09c -100 rgb 50 200 10

surf Sphere  sph 0 0 {offset_1} {diameter}
surf Sphere2 sph 0 0 {offset_2} {diameter}

surf box cube 0 0 0 {box_size}

cell Core 0 fuel -Sphere
cell Core2 0 fuel -Sphere2
cell Box 0 void Sphere Sphere2 -box

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
    if len(sys.argv) > 1:
        bins = sys.argv[1]
    else:
        bins = 4

    distances = np.linspace(0, 3, bins)
    filenames = []

    for distance in distances:
        sphere_diameter = 4.67

        parameters = {"diameter": str(sphere_diameter),
                      "offset_1": distance + sphere_diameter,
                      "offset_2": -distance - sphere_diameter ,
                      "box_size": 4 * sphere_diameter + 2 * distance}

        filename = "spheres_{distance:.3f}".format(distance=distance)
        filenames.append(filename)

        generate_file(filename, **parameters)

    results = []

    for file in filenames:
        results.append(run_serpent(file, options={"omp": 10}))

    print(results)
    k_effs = []

    for result in results:
        k_effs.append(get_multiplication_factor(result))

    figure = plt.figure(figsize=(16, 9))

    plt.plot(distances, k_effs, marker="o", color="r", label="Simulated k_eff")
    plt.legend()

    plt.xlabel("Distance between spheres")
    plt.ylabel("Neutron multiplication factor")

    plt.savefig("criticality.png", bbox_inches="tight", dpi=900)