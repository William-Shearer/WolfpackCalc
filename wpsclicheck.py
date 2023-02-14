from wpsclass import SubScen
from math import radians, degrees

"""
SubSig V.1.0
(CLI utility interface).
Wolfpack Simulation helper class/utility.
February 9, 2023. William Shearer.
misanthropus_ornatus@live.com
Please report bugs to GitHub user:
William-Shearer
MIT license.
"""

"""
This is a very simple CLI implementation of the SubScen class instance to debug.
Run it in the CLI with:
python wpsclicheckV1.py
Enter the data on the prompts and hit <ENTER>.
Uncomment the last line:
print(wps)
...to debug.
Change torpedoes right here in the code on line 37 to 41. The options are:
"G7a-lo" "G7a-md" "G7a-hi" "G7e-st"
Comment out as desired, leave only one uncommented.
"""
wps = SubScen()

# Data input segment.
wps.get_state["st_brg_A"] = radians(float(input("First bearing: ")))
wps.get_state["st_rng_A"] = float(input("First range: "))
wps.get_state["st_brg_B"] = radians(float(input("Second bearing: ")))
wps.get_state["st_rng_B"] = float(input("Second range: "))
wps.get_sub["hdg"] = radians(float(input("Sub heading: ")))
wps.get_sub["spd"] = float(input("Sub speed: "))
wps.get_state["s_time"] = float(input("Time: "))

# Set the desired torp here.
# wps.set_torp("G7a-lo")
# wps.set_torp("G7a-md")
# wps.set_torp("G7a-hi")
wps.set_torp("G7e-st")
# Look at the wpsclass.py file, dict _torps and function set_torp() to understand what is happening.

print("Torp Spd:", wps.get_weapon["spd"])
print("Torp Rng:", wps.get_weapon["max_rng"])

wps.mover(wps.get_sub, wps.get_state["s_time"], ("nx", "ny"))
wps.plotter()

print("Target Hdg:", round(degrees(wps.get_target["hdg"]), 2))
print("Target Spd:", round(wps.get_target["spd"], 2))

wps.torp_calculator()

print("Launch AOB:", round(degrees(wps.get_state["aob"]), 2))
print("Torp Hdg:", round(degrees(wps.get_weapon["hdg"]), 2))
print("Torp Rng:", round(wps.get_state["wpn_run"], 2))
print("Torp status:", wps.get_state["status"])
print("Impact:", round(degrees(wps.get_state["impact"]), 2))
# print(wps)