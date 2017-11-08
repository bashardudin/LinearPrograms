#!/usr/bin/env python
# _*_ encoding: utf-8 _*_

"""linprogs.py: Implements rational linear program object"""

import numpy as np
import fractions as frac

__author__ = "Bashar Dudin"
__email__ = "bashar.dudin@epita.fr"


class LinearProgram(object):

    def __init__(self, a, b, c, v=0):

        if not all(isinstance(i, np.ndarray) for i in (a, b, c)):
            raise TypeError("Arguments of numpy type array expected")

        if a.shape != (b.shape[0], c.shape[0]):
            raise TypeError("Arguments are not of coherent dimensions")

        m, n = a.shape

        # Storing slack form of input
        self.basic = [x for x in range(n, n+m)]
        self.shape = (m, n+m)

        self.table = np.zeros((m+1, n+m+1), dtype=frac.Fraction)
        self.table[0, :] = np.hstack((-c, np.zeros(m, dtype=frac.Fraction), np.array(v)))
        self.table[1:, :] = np.hstack((a, np.eye(self.shape[0], dtype=frac.Fraction), b))

    def __str__(self, width=4):
        """ Prints linear program to standard IO device.

        Useful if size of linear problem is reasonable.
        """
        # FIXME: Better alignement in case of fractions. Poorly supports formatting.

        def element_template(x, width=width):
            if isinstance(x, int):
                s = "{0: >{width}}".format(x, width=width+2)
            elif x.denominator == 1:
                s = "{0: >{width}}".format(x.numerator, width=width+2)
            else:
                s = "{0: >{width}}/{1:<}".format(x.numerator, x.denominator, width=width)
            s += " "*(2*width - len(s))
            return(s)

        template = ["   "]

        for j in range(self.shape[1]):
            template.append(element_template(self.table[0, j]))
        template.append("   {:>}\n\n".format(element_template(self.table[0, -1])))

        for i in range(self.shape[0]):
            template.append("{:>} |".format(self.basic[i]))
            for j in range(self.shape[1]):
                template.append(element_template(self.table[i+1, j]))
            template.append("   {:>}\n".format(element_template(self.table[i+1, -1])))
        return "".join(template)

    def basic_solution(self):
        """ Returns basic solution of linear program"""
        v = np.zeros(self.shape[1], dtype=frac.Fraction)
        for i in range(self.shape[0]):
            v[self.basic[i]] = self.table[i+1, -1]
        return v

    def has_feasible_basic(self):
        """ Checks if basic solution is feasible"""
        return all(self.basic_solution() >= 0)

    def pivot(self, index_in, index_out):
        """ Pivots linear program.

        Returns linear program equivalent ot input after exchanging roles of
        variables of respective indices index_in and index_out.

        :param index_in: index of column (in the tableau) entering into basic
        set of indices.
        :param index_out: index of line (in the tableau) leaving basic set of
        indices.
        :return: linear program equivalent to input.
        """
        a = self.table

        l = index_out
        e = index_in

        pivot = a[l, e]

        if self.shape[0] <= l <= 0 or self.shape[1] <= e < 0:
            raise ValueError("Indexes out of range")

        if pivot == 0:
            raise ValueError("Cannot pivot with given leaving and entering variables.")

        a[l, :] = a[l, :]/pivot

        for k in range(self.shape[0]):
            if k+1 != l:
                a[k+1, :] = a[k+1, :] - a[k+1, e]*a[l, :]
        a[0, :] = a[0, :] - a[0, e]*a[l, :]

        self.basic[l-1] = e

    def dual(self):
        """ Dual linear program

        :return: the dual linear program to a linear program.
        """
        # TODO: Write down dual linear program

        pass
