from math import cos, sin
from wpsutils import atan2f, Fn_Rng, aob_calc, invert

"""
SubSig V.1.0
(Class file)
Wolfpack Simulation helper class/utility.
February 9, 2023. William Shearer.
misanthropus_ornatus@live.com
Please report bugs to GitHub user:
William-Shearer
MIT license.
"""
class SubScen:
    """
    The Class. Established the various variables and functions that will be used to calculate
    a target's motion, as well as plotting the adequate topredo firing angle.
    Data is stored in Python dicts.
    All distances are in meters.
    """
    def __init__(self):
        
        """
        ox: the sub's original x position.
        oy: the sub's original y position.
        nx: the sub's new x position.
        ny: the sub's new y position.
        hdg: the sub's heading, in radians.
        spd: the sub's speed, in meters/second.
        """
        self._sub =     {   "ox": 0.0,
                            "oy": 0.0,
                            "nx": 0.0,
                            "ny": 0.0,
                            "hdg": 0.0,
                            "spd": 0.0          }
        
        """
        ox: the target's original x position.
        oy: the target's original y position.
        nx: the target's new x position.
        ny: the target's new y position.
        pgt_x: the target's propagated x position, for torpedo impact calculation.
        pgt_y: the target's propagated x position, for torpedo impact calculation.
        hdg: the target's heading, in radians.
        spd: the target's speed, in meters/second.
        """
        self._target =  {   "ox": 0.0,
                            "oy": 0.0,
                            "nx": 0.0,
                            "ny": 0.0,
                            "pgt_x": 0.0,
                            "pgt_y": 0.0,
                            "hdg": 0.0,
                            "spd": 0.0          }
        
        """
        nx: the weapon's new x position.
        ny: the weapon's new y position.
        hdg: the weapon's heading, in radians.
        max_rng: the weapon's maximum range, in meters.
        spd: the weapon's speed, in meters/second.
        """
        self._weapon =  {   "nx": 0.0,
                            "ny": 0.0,
                            "max_rng": 0,
                            "hdg": 0.0,
                            "spd": 0.0        }
        
        """
        st_brg_A: the sub to target (st) bearing on the A mark point, in radians.
        st_brg_B: the sub to target (st) bearing on the B mark point, in radians.
        st_rng_A: the sub to target (st) range, from the A mark point.
        st_rng_B: the sub to target (st) range, from the B mark point.
        torp_time: the time in seconds that the torpedo (weapon) has run. Used for the propagation function.
        status: Information to the user if the torp hits the target or runs out of steam (or battery) before reaching target.
        aob: the angle on bow, from the submarine heading to the target heading. Positive values are right bow.
        impact: the angle on bow of the torpedo heading to the target heading, at the moment when the torpedo hits the target.
        wt_rng: the range in meters from the torpedo (weapon) to the target (wt). Used during propagation.
        wpn_run: the distance the weapon has travelled. Propagated second by second, at the weapon's spd in meters/second.
        """
        self._state =   {   "st_brg_A": 0.0,
                            "st_brg_B": 0.0,
                            "st_rng_A": 0.0,
                            "st_rng_B": 0.0,
                            "torp_time": 0,
                            "s_time": 0,
                            "status": "--",
                            "aob": 0.0,
                            "impact": 0.0,
                            "wt_rng": 0.0,
                            "wpn_run": 0.0      }
                            
        """
        These are the basic stats for the torpedoes used in Wolfpack.
        As the sim adds others, the data can be added here, and updated in the GUI module list.
        The list here contains the following data:
        [0] torp speed, in meters/second.
        [1] torp max range, in meters.
        """
        self._torps =   {   "G7a-lo": [15.43, 12000],
                            "G7a-md": [20.57, 7500],
                            "G7a-hi": [22.63, 5000],
                            "G7e-st": [15.43, 5000]     }
                            
        
    def __del__(self):
        """
        Self-evident.
        """
        print("Instance deleted")
        
    def __str__(self):
        """
        Create and return the debug string.
        """
        description = "\nSUB:\n"
        for k, v in self._sub.items():
            description += f"{k}: {v:.2f}\n"
        description += "\nTARGET:\n"
        for k, v in self._target.items():
            description += f"{k}: {v:.2f}\n"
        description += "\nWEAPON:\n"
        for k, v in self._weapon.items():
            description += f"{k}: {v:.2f}\n"
        description += "\nSTATE:\n"
        for k, v in self._state.items():
            description += f"{k}: {(lambda a: a if isinstance(a, str) else f'{a:.2f}') (v)}\n"
        description += "\nTORPS:\n"
        for k, v in self._torps.items():
            description += f"{k} \nSpeed: {v[0]}\nRange: {v[1]}\n"
        return description
    
    """
    All properties are used to access the dicts. Dicts do not need a setter property.
    Simply obtaining (getting) the dict with the property, through the code that uses
    this class, and appending the ["key"] after using the property, like this...
    wps.get_sub["spd"] = 15.0
    ...will be enough to set that KV pair's value.
    """
    
    @property
    def get_sub(self):
        """
        Get the sub (submarine) dictionary.
        """
        return self._sub
    
    @property
    def get_target(self):
        """
        Get the target dictionary.
        """
        return self._target
        
    @property
    def get_weapon(self):
        """
        Get the weapon dictionary.
        """
        return self._weapon
        
    @property
    def get_state(self):
        """
        Get the state dictionary.
        """
        return self._state
        
    @property
    def get_torps(self):
        """
        Get the torps dictionary. Utilizing this particular property has an additional requirement.
        The key references (holds) a list, instead of a single value. Utilize the ["key"] and the index
        of the list [0] to retrieve the values. Like this...
        wps.get_torps["G7a-hi"][0]
        """
        return self._torps
        
    def mover(self, data, t, param):
        """
        This is a general purpose mover. It aacepts any of the mobile unit dictionaries (sub, target or weapon)
        provided that the correct param is used in the code, for example:
        mover(wps.get_sub, wps.get_state["s_time"], ("nx", "ny"))
        """
        data[param[0]] = sin(data["hdg"]) * data["spd"] * t # nx
        data[param[1]] = cos(data["hdg"]) * data["spd"] * t # ny
        
    def plotter(self):
        """
        This function plots the target position (x, y) from the two mark readings, thereby permitting
        the user to keep the submarine underway during the observation/mark procedure. The relative motion is accounted for.
        The speed and heading of the target is calculated and stored in the appropriate dict.
        For players, it is worth noting that this function, or any part of the program, corrects for
        their error in ranging. The challenge of a proper bearing/range mark procedure is still critical.
        """
        self._target["ox"] = (sin(self._state["st_brg_A"]) * self._state["st_rng_A"]) + self._sub["ox"]
        self._target["oy"] = (cos(self._state["st_brg_A"]) * self._state["st_rng_A"]) + self._sub["oy"]
        self._target["nx"] = (sin(self._state["st_brg_B"]) * self._state["st_rng_B"]) + self._sub["nx"]
        self._target["ny"] = (cos(self._state["st_brg_B"]) * self._state["st_rng_B"]) + self._sub["ny"]
        x_dist = self._target["nx"] - self._target["ox"]
        y_dist = self._target["ny"] - self._target["oy"]
        self._target["spd"] = Fn_Rng(x_dist, y_dist) / self._state["s_time"]
        self._target["hdg"] = atan2f(x_dist, y_dist)

    def set_torp(self, torp_type):
        """
        Sets the torpedo that will be used for calculation in the propagation segment.
        For players, it is important that the correct torpedo is used, according to what they intend to fire.
        """
        self._weapon["spd"] = self._torps[torp_type][0]
        self._weapon["max_rng"] = self._torps[torp_type][1]
    
    def torp_calculator(self):
        """
        This is the propagation function that eventually determines the bearing to launch the torpedo on.
        It also calculates an angle on bow. Therefore, the results of this function can be used either for
        zero gyro angle firing, or supplementary to a good TDC procedure.
        Players should understand how to do this, both ways, before identifying if this program is in error.
        Read the Wolfpack manual, if in doubt.
        Previously, I was using the Law of Sines method to calculate AOB, however, it has a drawback in that
        the ambiguous cases (eg: sines of 135 and 45 AOB return the same value). This method, even though it looks
        long wided, effectively solves this problem and correctly calculates lead angles and ranges, regardless of AOBs > 90.
        Additionally, it also informs the player whether the target is in range, and what the impact angle would be.
        Note, the impact angle is the AOB at which the torpedo strikes the target. It should be as perpendicular to
        the target center-line as possible (ie; 90 degrees).
        """
        self._target["pgt_x"] = 0.0
        self._target["pgt_y"] = 0.0
        self._state["wpn_run"] = 0.0
        self._state["torp_time"] = 0
        self._state["aob"] = aob_calc(invert(self._state["st_brg_B"]), self._target["hdg"])
        while True:
            self._state["torp_time"] += 1
            self.mover(self._target, self._state["torp_time"], ("pgt_x", "pgt_y"))
            self._target["pgt_x"] += self._target["nx"]
            self._target["pgt_y"] += self._target["ny"]
            x_dist = self._target["pgt_x"] - self._sub["nx"]
            y_dist = self._target["pgt_y"] - self._sub["ny"]
            self._weapon["hdg"] = atan2f(x_dist, y_dist)
            self.mover(self._weapon, self._state["torp_time"], ("nx", "ny"))
            self._weapon["nx"] += self._sub["nx"]
            self._weapon["ny"] += self._sub["ny"]
            x_dist = self._target["pgt_x"] - self._weapon["nx"]
            y_dist = self._target["pgt_y"] - self._weapon["ny"]
            self._state["wt_rng"] = Fn_Rng(x_dist, y_dist)
            self._state["wpn_run"] += self._weapon["spd"]
            
            if (self._state["wt_rng"] <= self._weapon["spd"]):
                self._state["status"] = "In Range"
                self._state["impact"] = aob_calc(invert(self._weapon["hdg"]), self._target["hdg"])
                break
            if (self._state["wpn_run"] > self._weapon["max_rng"]):
                self._state["status"] = "Out of Range"
                self._state["impact"] = 0.0
                break
