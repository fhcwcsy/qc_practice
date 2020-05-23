from sympy import *

def get_angles(a, b, c, d):
    if im(a) == 0:
        print("Not phasing")
        s = _compute_angles(a, b, c, d)
        res = _final_constraint(s)
        if len(res) != 0:
            return res
    print("Phasing by first element...")
    matr = Matrix([[a, b], [c, d]])
    ph = arg(matr[0])
    matr_phased = simplify(matr/(cos(ph) + I*sin(ph)))
    s = _compute_angles(matr_phased[0], matr_phased[1], matr_phased[2],
                        matr_phased[3])
    return _final_constraint(s)


def _compute_angles(a, b, c, d):
    theta, phi, lamb = symbols('\\theta \\phi \\lambda', real=True)
    a_eq = Eq(cos(theta / 2), a)
    b_eq = Eq(-exp(I * lamb) * sin(theta / 2), b)
    c_eq = Eq(exp(I * phi) * sin(theta / 2), c)
    d_eq = Eq(exp(I * (phi + lamb)) * cos(theta / 2), d)
    return solve([a_eq, b_eq, c_eq, d_eq], [theta, phi, lamb], dict=True)


def _final_constraint(result):
    res = []
    for sol in result:
        to_add = True
        for k, v in sol.items():
            if str(k) == '\\theta' and (v < 0 or v > pi):
                to_add = False
                break
            elif str(k) == '\\phi' and (v < 0 or v >= 2 * pi):
                to_add = False
                break
        if to_add:
            res.append(simplify(sol))
    return res 

if __name__ == "__main__":
    sqy = Matrix([[1+I, -1-I], [1+I, 1+I]]) * Rational(1,2) 
    print(get_angles(sqy[0], sqy[1], sqy[2], sqy[3]))
