# dimension_strs.py        -*- coding: utf-8 -*-

# Cabinet Wiz module for working with fractional dimension strings.

# Copyright © 2018  Harry H. Toigo II, L33b0

# This file is part of Cabinet Wiz, the ....

# Cabinet Wiz is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Cabinet Wiz is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Cabinet Wiz.  If not, see <https://www.gnu.org/licenses/>.

# To contact us:
#
# Email:       hhtpub@gmail.com
# Snail mail:  433 Buena Vista Ave. #310
#              Alameda CA  94501


from fractions import Fraction
import math

debug = False


# Interface


def dimstr(x):
    """Convert a floating point dimension to a fractional string representation.

    The value `x' is the measurement of a dimension. Its string representation
    is intended to be convenient for cutting in the shop. Some examples:

        `x'             Return Value
        11.375          '11 3/8'
        17.2683         '17 1/4+'
        34.285714...    '34 5/16-'

    Fractions are constrained to units of 1/n, where n is defined below, so
    results are reported to the nearest nth--i.e., if n equals 16, then results
    are reported to the nearest sixteenth. If x is not an exact number of nths,
    return the nearest nth in lowest terms (e.g. 1/4 instead of 4/16), with a
    `+' or `-' suffix indicating `strong' or `shy', respectively.
    """
    n = 16          # 16 means an nth is one sixteenth;
                    # 32 means an nth is one thirty-secondth, etc.

    # x = nths / n    (In general, `nths' will NOT be an integral value.)
    nths = x * n
    # Separate the number of 'nths' into integral & fractional parts:
    nths_frac, nths_int = math.modf(nths)
    # Change nths_int/n into the mixed number `i nths_int/n':
    #     from 546/16      to    34 2/16
    #          nths_int/n        i  nths_int/n
    i, nths_int = divmod(int(nths_int), n)
    lowernth_frac = Fraction(nths_int, n)
    uppernth_frac = Fraction(nths_int + 1, n)
    if debug:
        print('i=' + str(i))
        print('nths_int=' + str(nths_int))
        print('n=' + str(n))
        print('nths_frac=' + str(nths_frac))
        print('lowernth_frac=' + str(lowernth_frac))
        print('uppernth_frac=' + str(uppernth_frac))

    if nths_frac < 0.25:
        # Within 1/4n of the lower nth--1/64, in the usual case of n=16. We are
        # less than halfway to the midpoint between the lower and upper nths, so
        # we drop the `strong'.
        result = lowerval_str(i, lowernth_frac)
    elif nths_frac < 0.5:
        # Closer to the lower nth than the upper.
        result = lowerval_strong_str(i, lowernth_frac)
    elif nths_frac == 0.5:
        # Exactly in the middle; `round' to the even value with `strong' or
        # `shy', as required.
        if is_even(nths_int):
            result = lowerval_strong_str(i, lowernth_frac)
        else:
            result = upperval_shy_str(i, uppernth_frac)
    elif nths_frac <= 0.75:
        # Closer to the upper nth than the lower.
        result = upperval_shy_str(i, uppernth_frac)
    else:
        # nths_frac > 0.75. Within 1/4n of the upper nth--1/64, if n=16.
        # Consequently, we drop the `shy'.
        result = upperval_str(i, uppernth_frac)
    return result


def dimstr_col(x):
    """Like dimstr(x), adjusted so whole number parts align in columns."""
    return sdalign( dimstr(x) )


# Implementation


def sdalign(str):
    """Align a single-digit number with column of double-digit numbers.

    Indent strings such as `4' or `8 3/4', to align whole number parts with
    numbers like `22 3/8', as follows:

        22 3/8                   22 3/8
         8 3/4    rather than    8 3/4
         4                       4
    """
    if len(str) == 1 or str[1] == ' ':
        result = ' ' + str
    else:
        result = str
    return result


def is_even(num):
    return (num % 2 == 0)


def lowerval_str(i, frac):
    """Return a string for an exact lower fractional value.

    `i' is an integer, and `frac' is an instance of Fraction.
    """
    if frac == 0:
        # The fractional part is 0, so just use the integer. If the entire value
        # is 0, we want the result to be `0'.
        result = str(i)
    elif i == 0:
        # We want `3/4' instead of `0 3/4'.
        result = str(frac)
    else:
        result = str(i) + ' ' + str(frac)
    return result


def lowerval_strong_str(i, frac):
    """Return a string for a `strong' lower fractional value.

    `i' is an integer, and `frac' is an instance of Fraction. Since this
    function is used for lower nths only, `frac' can be 0 but cannot be 1. So
    the logic is the same as for lowerval_str.
    """
    return lowerval_str(i, frac) + '+'


def upperval_str(i, frac):
    """Return a string for an exact upper fractional value.

    `i' is an integer, and `frac' is an instance of Fraction.
    """
    if frac == 1:
        # The fractional part is 1, so move up to the next integer.
        result = str(i + 1)
    elif i == 0:
        # We want `3/4' instead of `0 3/4'.
        result = str(frac)
    else:
        result = str(i) + ' ' + str(frac)
    return result


def upperval_shy_str(i, frac):
    """Return a string for a `shy' upper fractional value.

    `i' is an integer, and `frac' is an instance of Fraction. Since this
    function is used for upper nths only, `frac' can be 1 but cannot be 0. So
    the logic is the same as for upperval_str.
    """
    return upperval_str(i, frac) + '-'


# dimension_strs.py ends here
