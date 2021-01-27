import numpy as np


class Particle:
    p = 0
    y = 0
    phi = 0

    def __init__(self, _p, _y, _phi):
        self.p = _p
        self.y = _y
        self.phi = _phi

    def get_pt(self):
        pt = self.p / np.cosh(self.y)

        return pt

    def delta_squared(self, particle2):
        return (self.y - particle2.y) ** 2 + (self.phi - particle2.phi) ** 2

    def d_ij(self, particle2, exp=-2, R=0.5):
        return min(self.get_pt() ** exp, particle2.get_pt() ** exp) * self.delta_squared(particle2) / R

    def d_B(self, exp = -2):
        return self.get_pt()**exp

    def __str__(self):
        return str("p = {}, y = {}, phi = {}".format(self.p, self.y, self.phi))

    def __add__(self, other):
        p = self.p + other.p

        pt = self.get_pt() + other.get_pt()
        pl = np.sqrt(p**2 - pt**2)
        y = np.arctanh(pl/abs(p))

        phi = (self.phi + other.phi)/2.0

        return Particle(p, y, phi)


p1 = Particle(15.0, 2.0, 3.0)
p2 = Particle(8.0, 2.1, 3.1)
p3 = Particle(7.0, 1.9, 2.8)
p4 = Particle(1.2, 1.8, 3.14)
p5 = Particle(20.0, 1.3, 1.7)
p6 = Particle(4.0, 1.35, 1.6)
p7 = Particle(3.0, 1.0, 1.8)
p8 = Particle(2.0, 1.5, 1.65)
p9 = Particle(1.0, 1.1, 1.1)

ps = [p1, p2, p3, p4, p5, p6, p7, p8, p9 ]

jets = []

if __name__ == "__main__":

    while len(ps) > 0:
        for p1 in ps:

            min_d = np.infty
            min_p1 = None
            min_p2 = None

            for p2 in ps:
                if p1 is not p2:

                    d = p1.d_ij(p2)

                    if d < min_d:
                        min_d = d
                        min_p1 = p1
                        min_p2 = p2

            if p1.d_B() < min_d:
                ps.remove(p1)
                jets.append(p1)
            else:
                p_temp = min_p1 + min_p2

                print("Summed:")
                print(min_p1)
                print(min_p2)
                print("to")
                print(p_temp)

                ps.remove(min_p1)
                ps.remove(min_p2)
                ps.append(p_temp)

    print("Jets:")

    for jet in jets:
        print(jet)
