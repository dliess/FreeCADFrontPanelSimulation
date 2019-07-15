# FreeCAD Front Panel Simulation Workbench

## Description
With this FreeCAD addon one can turn their FreeCAD objects into knobs, faders, displays, etc... that in turn can be manipulated (pushed/moved/turned) via the mouse and that provides/receives data to an external application via grpc. 

Featured widgets:
* Rotary encoders (also with push-button functionality)
* Rotary potentiometer (also motorized, optional snap-in divisions)
* Pushbuttons(also in switch mode)
* Linear potentiometers (also motorized, optional snap-in divisions)
* LEDs
* Displays(Points, Lines, Rectangles, Bitmaps, Text)
* Touch-surface


![Overview](/icons/overview.png?raw=true)
![Screenshot1](/Examples/draw-toy/screenshots/Push2_1.png?raw=true)
![Screenshot2](/Examples/draw-toy/screenshots/Push2_2.png?raw=true)
![Screenshot3](/Examples/draw-toy/screenshots/draw-toy1.png?raw=true)
![Screenshot4](/Examples/draw-toy/screenshots/draw-toy2.png?raw=true)
![Screenshot5](/Examples/draw-toy/screenshots/draw-toy3.png?raw=true)
![Screenshot6](/Examples/draw-toy/screenshots/draw-toy4.png?raw=true)


# Prerequisites:

## Linux (tested on Ubuntu 18.04)
Minimum FreeCAD version: 0.18 (maybe v0.17 also (did not test it with that) v0.16 did not work)
```
sudo apt-get install python-concurrent.futures
sudo apt-get install python-pip
python -m pip install --upgrade pip
sudo python -m pip install grpcio
python -m pip install --user grpcio-tools
```
    
# Installation
Currently to test this workbench you need to clone it in to your `~/.FreeCAD/Mod` directory. 
```
cd ~/.FreeCAD/Mod/
git clone https://github.com/dliess/FreeCADFrontPanelSimulation
cd ~/.FreeCAD/Mod/FreeCADFrontPanelSimulation/grpc/python
make
sudo make install
```  
**Note:** `make` generates grpc-files for clients and server

# Test the Workbench
You can test the FreeCAD Front Panel Simulation workbench using the prebundled `draw-toy` example.  
* Start freecad-daily
* Load `draw-toy.fcstd`
* Switch to Frontpanel-simulation workbench
* Press Start button (green arrow symbol)
* From a terminal:change to application directory, then do  PYTHONPATH=/path/to/repo ./draw-toy-app.py`  
* Start turning/pushing knobs and faders, change display resolution(needs app-restart)

# Usage
[Wiki](https://github.com/dliess/FreeCADFrontPanelSimulation/wiki)

# Future Todos
* Some kind of automation to cut out holes with tolerance through front panel for the widgets (Ideas are welcome!)
* Example with c++ Application code (SSD1331 Oled display + Arduino Adafruit demo code + grpc-patched Adafruit driver)
* Midi Sequencer/Midi-Controller Example (Controlling a HW-Synthesizer)
* Map Keyboard keys to Button Widgets
* Render QT-Framebuffer into display widgets

# Problems/Workarounds:
* Setting `pixel 0,0` causes border of display to be set with the color of the pixel  
   Workaround: Cover `0,5 mm` of the display border with the front panel

# Author
[@dliess](https://github.com/dliess)

# Feedback 
Please open an issue in the Issue queue. To discuss the workbench please post to the dedicated FreeCAD [forum thread](https://forum.freecadweb.org/viewtopic.php?f=24&t=29988).

# License
MIT License

Copyright (c) 2019 dliess

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
