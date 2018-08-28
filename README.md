# OTS Randomizer
A simple program for randomizing different aspect of the levels in the game Out There Somewhere.

## How to install?
Download the latest version from [releases](https://github.com/thisishowmymindworks/ots-randomizer/releases) and move it into the install folder for OTS. Then you can simply run it from there, or create a short-cut on your desktop for easier access.

##  Requirements
- Python 3.5+
- [Toga ](https://pypi.org/project/toga/) for GUI elements
- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/) for XML parsing
- [PyInstaller](https://pypi.org/project/PyInstaller/) for building to an executable

## Running/building
Assuming you have installed all the requirements you can simply run the [randomizer.py](https://github.com/thisishowmymindworks/ots-randomizer/blob/master/randomizer.py "randomizer.py") file directly to run the randomizer. You will need to edit the ots_path at the top of the file to point to your own OTS install folder for it to work correctly.

To build the file to a single executable you can run the command `PyInstaller randomizer.spec -F` You can find the executable in the *dist* folder, but you will need to move it to the OTS install folder for the program to run correctly.

## Acknowledgments
- [Pedro Medeiros (saint11)](https://twitter.com/saint11) - Programmer and artist for OTS
- [Amora B. (amora_b)](https://twitter.com/amora_b) - Aritst and writer for OTS
- The entire OTS speedrunning community, you're all wonderful ^^
