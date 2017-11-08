#!/usr/bin/env python
# _*_ encoding: utf-8 _*_

"""simplex.py: Simplex algorithm with rational coefficients"""

import numpy as np
import fractions as frac

__author__ = "Bashar Dudin"
__email__ = "bashar.dudin@epita.fr"


class RestrictedSimplex(object):

    def __init__(self, leaving_index=None, entering_index=None):
        if not leaving_index:
            def func(l):
                m = 0
                while not l[m] and m < len(l):
                    m += 1
                if m == len(l):
                    return 0
                for i in range(len(l)):
                    if l[i] and l[m] > l[i]:
                            m = i
                return m
            leaving_index = func

        if not entering_index:
            def func(l):
                return l.index(min(l))
            entering_index = func

        self.leaving_index = leaving_index
        self.entering_index = entering_index

    def __call__(self, lin_p, recursion_limit=100):
        """ Runs a restricted version of the simplex algorithm

        Runs simplex algorithm on linear programs having feasible basic
        solution. It takes in an integer to limit the number of recursions.

        :return: a linear program whose basic solution has maximal objective
        value.
        """
        a = lin_p.table

        if not lin_p.has_feasible_basic:
            raise TypeError("Linear program doesn't have feasible base solution")

        n = 0
        while any(a[0, :-1] < 0) and n < recursion_limit:
            entering_choices = [i for i in map(lambda x: 0 if x > 0 else x,
                                a[0, :-1])]
            e = self.entering_index(entering_choices)

            leaving_choices = [None]*lin_p.shape[0]
            for i in range(lin_p.shape[0]):
                if a[i+1, e] > 0:
                    leaving_choices[i] = (a[i+1, -1]/a[i+1, e])
            if not [i for i in leaving_choices if i]:
                raise OverflowError("Linear program unbounded | check model and state.")
            else:
                l = 1 + self.leaving_index(leaving_choices)

            lin_p.pivot(e, l)
            n += 1

        form = "Basic solution = " + \
               "(" + "{}, " * (lin_p.shape[1] - 1) + "{})" + \
               " with objective value = {}."
        print(form.format(*lin_p.basic_solution(), lin_p.table[0, -1]), end="\n\n")

        return lin_p.basic_solution(), lin_p.table[0, -1]


class Simplex(RestrictedSimplex):

    def is_feasible(self, lin_p):
        """ Checks if linear program is feasible..

        Has side effect: transforms linear program if not basic feasible
        into an equivalent linear program having basic feasible solution.

        :return: boolean.
        """

        print(" ### Checking feasibility of linear program", lin_p, sep="\n\n")

        if lin_p.has_feasible_basic():
            print(" ### Input linear program has feasible basic solution", end="\n\n")
            return True

        print(" ### Basic solution is not feasible: using auxiliary linear program in next step", end="\n\n")

        gain_fun = np.copy(lin_p.table[0])

        lin_p.shape = (lin_p.shape[0], lin_p.shape[1] + 1)
        lin_p.table = np.insert(lin_p.table, 0, frac.Fraction(-1, 1), axis=1)
        lin_p.table[0] = np.hstack((np.ones(1, dtype=frac.Fraction),
                                    np.zeros(lin_p.shape[1], dtype=frac.Fraction)))
        lin_p.basic = [i+1 for i in lin_p.basic]

        l = 1 + np.argmin(lin_p.table[1:, -1])
        lin_p.pivot(0, l)  # Now program has feasible basic solution

        if RestrictedSimplex.__call__(self, lin_p)[1] == 0:
            print(" ### Input linear program is thus feasible", end="\n\n")

            if 0 in lin_p.basic:
                l = lin_p.basic.index(0)

                e = 0
                while e < lin_p.shape and lin_p.table[l, e] == 0:
                    # There is a at least an e with this property
                    # Unbounded otherwise
                    e += 1
                lin_p.pivot(e, l)  # 0 not basic anymore

            lin_p.basic = [i-1 for i in lin_p.basic]
            lin_p.table = lin_p.table[:, 1:]
            lin_p.shape = (lin_p.shape[0], lin_p.shape[1] - 1)

            lin_p.table[0] = gain_fun
            for i in lin_p.basic:
                lin_p.table[0, :] = lin_p.table[0, :] - \
                                      lin_p.table[0, i] * \
                                      lin_p.table[1 + lin_p.basic.index(i), :]
            lin_p.table[0, -1] = -lin_p.table[0, -1]

            return True

        else:
            return False

    def __call__(self, lin_p, recursion_limit=100):
        """ Simplex algorithm.

        :return: a linear program whose basic solution has maximal objective
        value.
        """
        if self.is_feasible(lin_p):
            simplex = RestrictedSimplex(self.leaving_index,
                                        self.entering_index)

            print(" ### Getting back to linear program equivalent to input with feasible basic solution", end="\n\n")
            return simplex(lin_p, recursion_limit=recursion_limit)

        else:
            raise Exception("Linear program is not feasible.")
