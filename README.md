# Wolfpack Solution Calculator
## Version 1.0
A utility aid for the game Wolfpack, a submarine simulator by Usurpator AB / SubSim.
February 9, 2023. William Shearer.  

### Quick Start  
1. Install or clone the utility from the repo (see below for details).  
2. Start the application by double clicking the wpsgui.pyw file.  
3. Enter the submarine data:
	* Set submarine heading in first compass rose (click to set general bearing, fine tune with mousewheel).  
	* Use slider below to set submarine speed in knots.  
4. Enter the first bearing and range to the target (Mark A) with the second compass rose. Use same method as above.  
5. Allow time to elapse, and enter the second bearing and range to the same target (Mark B) in the last compass rose.  
6. Set the time between the taking of Mark A and Mark B with the Mark Time (seconds) slider. To the right you will see seconds convered to M:SS.  
7. Select the type of torpedo that will be fired at the target from the dropdown list.  
8. Hit EXECUTE button.  
9. Calculated solution data will be shown in the SOLUTION window at the bottom. It assumes firing immediately.  
	* If the target in range of the selected torpedo type.  
	* The heading of the target, relative to north.  
	* The Angle on the Bow at Mark B.  
	* The impact angle, in angle on the bow, after the torpedo reaches the target (if in range).  
	* The time it will take the torpedo to reach the target.  
	* The distance the torpedo will cover to reach the target (if out of range, this number will be the torpedo max range).  
	* The torpedo heading, realtive to north.  
	* The realtive bearing, in relation to the longitudinal axis of the submarine, that the torpedo will fire on.  




Please report bugs to GitHub user:  
William-Shearer  
MIT license.  
  
