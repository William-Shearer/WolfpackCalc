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


def gyro_angle(brg, hdg):
    """
    Takes a bearing and a heading a returns a relative bearing.
    Where aob needs negative left, positive right, this should be a relative bearing on 360 degrees (pi * 2).
    Small difference...
    """
    ga = brg - hdg
    if ga < 0.0:
        ga += (pi * 2)
    elif ga >= (pi * 2):
        ga -= (pi * 2)
    return ga


def convert_to_ms(kt):
    # Converts knots to meters per second
    return kt / 1.944
    

def convert_to_kt(ms):
    # Converts meters per second to knots.
    return ms * 1.944
    

def convert_to_meters(hm):
    # Converts hecto-meters to meters.
    return hm * 100
    

def convert_to_hm(m):
    # Converts meters to hecto-meters.
    return m / 100


def gen_min_conv(sec):
    # Returns string minutes formatted 0:00
    try:
        fsec = float(sec)
    except ValueError:
        return "0"
    dec_mins = fsec / 60.0
    return f"{int(dec_mins)}:{round((dec_mins - int(dec_mins)) * 60):02}"
    
"""
Lambda function, all it does is Pythagoras, to calculate a range from given coordinates.
"""
Fn_Rng = lambda x, y: sqrt(pow(x, 2) + pow(y, 2))
