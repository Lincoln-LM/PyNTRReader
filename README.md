# PyNTRReader
 Python Lib for reading information from 3ds Pokémon games

 The structure of this tool is based on PyNXBot by [wwwwwwzx](https://github.com/wwwwwwzx) so credit to them and other who worked on the original project!

## Features
 * Read Wild Pokémon info in Gen 6
 * Read Radar Pokémon info in Gen 6
 * Read Egg Seeds in Gen 6
 * Read TinyMT Seeds and track index in Gen 6
 * Read TinyMT Seeds and Initial Seed with breakpoints in Gen 6 (iffy)
 * Read Transporter Pokémon info
 * Read Wild Pokémon info in GS
 * Read Wild Pokémon info in GS

## Requirements
* [Python](https://www.python.org/downloads/)
	* Install pillow and pokebase via [pip](https://pip.pypa.io/en/stable/) if `ImportError` happens.
	   `pip install pillow`
	   `pip install pokebase`
* CFW
* Internet Connection

## Usage
* Edit ip.py with your 3ds IP Address
* Scripts labeled "read_'name'.py" will display info on that type of encounter in the console
* Scripts labeled "GUI'Name'.py" will display info on that type of encounter in a tkinter GUI

## Credits:
* [wwwwwwzx](https://github.com/wwwwwwzx) for PyNXBot and 3dsRNGTool
