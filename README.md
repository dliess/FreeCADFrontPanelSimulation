![Overview](/icons/overview.png?raw=true)
![Screenshot1](/Examples/draw-toy/screenshots/Push2_1.png?raw=true)
![Screenshot2](/Examples/draw-toy/screenshots/Push2_2.png?raw=true)
![Screenshot3](/Examples/draw-toy/screenshots/draw-toy1.png?raw=true)
![Screenshot4](/Examples/draw-toy/screenshots/draw-toy2.png?raw=true)
![Screenshot5](/Examples/draw-toy/screenshots/draw-toy3.png?raw=true)
![Screenshot6](/Examples/draw-toy/screenshots/draw-toy4.png?raw=true)

# Basic description
With this FreeCAD plugin, you can turn your FreeCAD objects into knobs, faders, displays, etc. that you can push/move/turn by your mouse and that provides/receives data to an external application via grpc. 

Featured widgets:
* Rotary encoders (also with push-button functionality)
* Rotary potentiometer (also motorized, optional snap-in divisions)
* Pushbuttons(also in switch mode)
* Linear potentiometers (also motorized, optional snap-in divisions)
* LEDs
* Displays(Points, Lines, Rectangles, Bitmaps, Text)
* Touch-surface

# Prerequisites:

## Linux (tested on ubuntu 18.04):
* sudo apt-get install python-concurrent.futures
* sudo apt-get install python-pip
* python -m pip install --upgrade pip
* sudo python -m pip install grpcio
* python -m pip install --user grpcio-tools
* Minimum FreeCAD version: 0.18 (maybe 0.17 also, did not test it with that, 0.16 did not work)
* For the [c++ GRPC installation](https://github.com/grpc/grpc/blob/v1.14.1/src/cpp/README.md) 
  - Prerequisites:
    - sudo apt-get install build-essential autoconf libtool pkg-config curl golang libssl-dev
      build and install the grpc components 
  - Clone grpc repo:
    - git clone https://github.com/grpc/grpc
  - Build third_party dependencies first as package, its the only way grpc will work with cmake find_package mechanism
    [link](https://github.com/grpc/grpc/issues/16741)
    - git submodule update --init
    - Attention: if boringssl does not compile. you need to checkout master of the boringssl lib
    - Build and install ZLIB
       - mkdir build; cd build
       - cmake -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Release ..
       - make && sudo make install 
    - [Install Protoc](https://github.com/protocolbuffers/protobuf/blob/master/cmake/README.md):
      - cd grpc/third_party/protobuf/cmake
      - mkdir -p  build/release; cd build/release
      - cmake -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Release -Dprotobuf_BUILD_TESTS=OFF ../..
      - make && sudo make install
    - Install OPENSSL
      - should already be installed, if not install with package manager
    - Install C-Ares
      -	cmake files in "third_party/cares/cares"
      - cmake -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Release ..
 - Build and install GRPC
    - mkdir build
    - mkdir build/release
    - cd build/release
    - cmake -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Release -DgRPC_ZLIB_PROVIDER=package -DgRPC_CARES_PROVIDER=package -DgRPC_PROTOBUF_PROVIDER=package -DgRPC_SSL_PROVIDER=package ../..
    - make
    - sudo make install

# Installation:
* cd ~/.FreeCAD/Mod/
* clone https://github.com/dliess/FreeCADFrontPanelSimulation
* cd ~/.FreeCAD/Mod/FreeCADFrontPanelSimulation/grpc/python
* make (this generates grpc-files for clients and server)

# Start Examples(draw-toy):
* Start freecad-daily
* Load draw-toy.fcstd
* Switch to Frontpanel-simulation workbench
* Press Start button (green arrow symbol)
* From a terminal:change to application directory, then do PYTHONPATH=/path/to/repo ./draw-toy-app.py
* Start turning/pushing knobs and faders, change display resolution(needs app-restart)

# Usage:
[Wiki](https://github.com/dliess/FreeCADFrontPanelSimulation/wiki)

# Future Todos:
* Some kind of automation to cut out holes with tolerance through front panel for the widgets(Ideas are welcome!)
* Example with c++ Application code (SSD1331 Oled display + Arduino Adafruit demo code + grpc-patched Adafruit driver)
* Midi Sequencer/Midi-Controller Example (Controlling a HW-Synthesizer)
* Map Keyboard keys to Button Widgets
* Render QT-Framebuffer into display widgets

# Problems/Workarounds:
* Setting pixel 0,0 causes border of display to be set with the color of the pixel
   Workaround: Cover 0,5 mm of the dispaly border with the front panel
