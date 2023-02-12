from math import atan, sqrt, pi

"""
SubSig V.1.0
Wolfpack Simulation helper class/utility.
February 9, 2023. William Shearer.
misanthropus_ornatus@live.com
Please report bugs to GitHub user:
William-Shearer
MIT license.
"""

def atan2f(x, y):
    """
    Modifies the behavior of standard atan to handle hemisphere error.
    Additionally, it handles the Division by Zero problem.
    I know it looks funny that it is handled by addressing x instead of y, 
    but there is logic behind the madness.
    If the error occurs on y being zero, x is checked to deterimine whether
    the result should be 90 or 270 degrees (equivalent in radians).
    """
    try:
        a = atan(x / y)
    except:
        if x >= 0.0:
            return pi * 0.5
        else:
            return pi * 1.5
            
    if x > 0 and y < 0:
        a = pi + a
    if x <= 0 and y < 0:
        a += pi
    if x <= 0 and y > 0:
        a = (pi * 2) + a
    return a


def invert(brg):
    """
    Creates an inverse bearing, given a true bearing.
    This function is a convenience, to avoid having to invert in the main code,
    or otherwise add code to deal with using a true bearing instead.
    """
    if (brg - pi) > 0.0:
        return brg - pi
    else:
        return (brg - pi) + (pi * 2)


def aob_calc(brg, hdg):
    """
    Obtain the angle on bow figure. Corrects for zero radian transition.
    """
    aob = brg - hdg
    if aob > pi:
        aob -= (pi * 2)
    elif aob < (-1 * pi):
        aob += (pi * 2)
    return aob

"""
Lambda function, all it does is Pythagoras, to calculate a range from given coordinates.
"""
Fn_Rng = lambda x, y: sqrt(pow(x, 2) + pow(y, 2))
