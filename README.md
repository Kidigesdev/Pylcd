This is a script with which ypu can display your PC stats on a Raspberry Pi 4B with a 2004 LCD Display.
You need an external MQTT Server (mine is in Homeassistant) to transfer the data.

**At this moment it supports only AMD GPU's!!**

**I only testet this Script on Linux!!**

Requirements on your PC:
  - pyamdgpuinfo library
  - Json library
  - psutil library
  - pahomqttclient library

Requirements on your Pi:
  - Json library
  - pahomqttclient library
  - RPLCD.i2c

Optinally I created a version which changes the output from static PC data to the Bitcoin worth data. 
This is the LCD-BTC.py

***BETA***
In the Beta folder is a windows version with NVIDIA GPU support of the data.py. I have not testet it and cannot tell if it works correctly!
